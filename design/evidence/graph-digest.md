# Graph digest

Named systems, mechanisms, attacks and bounds extracted from the corpus, ordered by how many papers discuss them. Paper keys are file stems; look them up in papers.tsv.

## Publish/Subscribe  [concept_publish_subscribe]  (concept; 510 papers)
Subscribers register continuous queries; an event service matches incoming publications to subscriptions and sends notifications for matches. Interaction is unidirectional and asynchronous through subscribe, publish, and notify operations; publisher and subscriber identities and locations are mutually unknown through the service.
Papers: 1998_chor_pir, 2004_borisov_otr, 2005_ostrovsky_streamingsearch, 2006_ishai_cryptography_from_anonymity, 2010_corrigangibbs_dissent, 2010_pfitzmann_terminology, 2011_carzaniga_contentbased, 2011_chen_scaling_construction
- assumes: Subjective trust ratings
- compares_with: Content-Based Pub/Sub; Private Information Retrieval; Scribe
- extends: Content-Based Pub/Sub; Topic-Based Pub/Sub
- implements: Inter-domain data-centric pub/sub architecture; Presence service; Topic-Connected Overlay; Two-layer hybrid architecture; Unstructured P2P overlay
- instance_of: Content-Based Pub/Sub; Delay-tolerant networks; Flow initiation patterns; Mobile Ad Hoc Network (MANET); Multicast; Social overlays; Topic-Based Pub/Sub
- leaks: Control Plane Visibility
- measures: Rendezvous latency result; Tree Diagnostic Metrics
- provides: Algorithm-Agnostic ALM Usage; Availability goal; Broker-mediated entity decoupling; Client decoupling and identity opacity; Concurrent Multicast Trees; Cover-based greedy rewriting; Metadata Privacy; Node Statistics; Publish/Subscribe Decoupling; Publish/Subscribe Tree (PST)
- requires: Broadcast Encryption; Low node degree objective; Message content visible to network; Overlay Network
- uses: Any-Source Multicast Forwarding; Broker overlay; Broker-based pub/sub middleware; Channel and episode organization; Content notification; Dedicated brokers; Dynamic forwarding paths; Event Notification Service; Event notification service; Event service

## Traffic Analysis  [concept_traffic_analysis]  (attack; 242 papers)
An observer uses visible network metadata and traffic features to infer identities, patterns, contents, or endpoints even when payloads are encrypted. PriFi aims to make honest users’ communication patterns indistinguishable, while leaving aggregate volume and packet time series visible.
Papers: 2009_danezis_sphinx, 2010_corrigangibbs_dissent, 2011_polyzos_contextaware, 2012_bip37_bloomfilter, 2012_bitmessage_wiki_changelog, 2012_elahi_guards, 2012_feigenbaum_onion_blackbox, 2012_mulamba_design
- assumes: Sibling AS collusion
- attacks: Anonymity as non-disclosure; Anonymous dissident linkage; Black-box functionality; Encryption-time leakage requirement; Fixed observable communication pattern; I2P; Location privacy; Mailbox ID computation; Metadata Privacy; Mixer nodes
- compares_with: Contextual attacks
- defends_against: Cover traffic; Traffic obfuscation
- extends: Traffic watermarking attack; Website Fingerprinting
- implements: Event-based detector
- instance_of: Client IP linkage; Colluding server correlation attack; Correlation attack vulnerability; DNS censorship and poisoning; Eavesdropper adversary; Eavesdropping; Flooding attacks; Network traffic correlation; Offline access-count inference; Self-signed certificate substitution
- leaks: Adaptive source posterior; BitTorrent; Metadata Privacy; Packet-size metadata leakage
- measures: Classification on real user visits; Effect of network location; Mobile call trace; Timing traffic features
- motivates: Author anonymity; Round-based requests; Topology knowledge enables attacks
- provides: Behavioral profiling; Relationship inference; Synthetic delivery latency result; Website Fingerprinting; Write-private database scheme
- requires: Low base-rate false alarms
- uses: Active routing attack threat; Deanonymization DoS Attack; Global adversary observations; Global traffic observer; Inter-packet delay; Semi-open-world targeting; Traffic features; Traffic trace features

## Topic-Based Pub/Sub  [concept_topic_based_pub_sub]  (system; 247 papers)
Publishers annotate each event with a topic string, generally a rooted path in a subject tree; subscribers specify topics, optionally using wildcards, and receive related events. The tree restricts classification to a single path, and associating an event with several hierarchical topics can cause duplicate publications and notifications and more exchanged information.
Papers: 2011_chen_scaling_construction, 2011_giannaki_supporting, 2011_guidec_communicationbasee, 2011_hosoda_approximability_minimum, 2011_hu_self_organizing, 2011_malekpour_endtoend, 2011_nguyen_swarmintelligent, 2011_pace_gossiping
- compares_with: Attribute-based pub/sub; Content-Based Pub/Sub; Epidemic and peer-to-peer reliability; Workflow control-event dissemination
- contradicts: Quality-of-context filtering; Security and privacy scope
- extends: Hierarchical topic namespaces; Hybrid topic and content filtering
- implements: Auditors; Bloom Filter; Edge broker model; IPv6 topic and priority encoding; Skip ring
- improves_on: Multicast; Rank-cover
- instance_of: Content-Based Pub/Sub; Delay-tolerant networks; EventCloud proxy flavors; High-dimensional pub/sub data; PubSubCoord; Publish/Subscribe; Scribe; Whisper
- part_of: Publish/Subscribe
- provides: Broker-mediated dissemination; Consensus reduction to local total order; Filter predicate; HTTPS hides gossip payload from intermediaries; HoPP robustness and resilience; Latest-publication reliability; Matching cost by language; Peer discovery; Resource Allocation Problem; Small local views
- requires: Filtering overhead and expressiveness trade-off; Unique message identifiers
- uses: Bayeux protocol; Event Type Schema; Event notification service; Event timestamps; Event-type-level configuration; Interest matrix; Lexicographic indexing; Multicast traffic and delay cost; OpenFlow topic and priority forwarding; Prefilter algorithm variants

## Tor  [concept_tor]  (system; 201 papers)
An onion-routing protocol described as faster and having little computational overhead, making it suitable for low-latency applications such as web browsing. It uses many volunteer nodes, most known to the routing decision maker, but the complete network view may limit scalability.
Papers: 2010_corrigangibbs_dissent, 2012_backes_provably_secure_onion, 2012_bitmessage_wiki_changelog, 2012_bitmessage_wiki_faq, 2012_elahi_guards, 2012_feigenbaum_onion_blackbox, 2012_mulamba_design, 2013_backes_anoa
- attacks: Entry guard compromise event; Low-resource descriptor harvesting; Tor exit banning; Traffic Analysis; Traffic analysis; Website fingerprinting
- compares_with: Curious event service; Verdict
- contradicts: Address leakage from one filter
- defends_against: Network metadata leakage; Traffic Analysis
- extends: Three-server Riposte
- hides: Server cannot link stored files to owners; s-server Riposte
- implements: Onion Routing; Tor Exit policy selection; Tor Guard selection; Tor three-hop circuit
- instance_of: Mixnet; Onion Routing; Publish/Subscribe; Secure onion algorithms; Tor traffic-based anonymity failure
- leaks: Entry guard observability; Traffic Analysis; Traffic pattern analysis
- measures: Directory refresh interval
- provides: Destination targeting; Entry guard rotation; Location privacy objective; Publisher and subscriber anonymity; Responder anonymity; Six-hop final circuit; Top relay selection share; Tor circuit hop count; Tor hidden-service rendezvous; Tor stream timeout policy
- requires: TCP reliable transport
- uses: Asynchronous publisher-subscriber exchange; Directory consensus admission; Distributed Hash Table; Entry Guards; Entry guards; Introduction authentication key match; Onion Routing; Persistent-connection decay model; Proxy and encryption assumption; Relay consumption-rate regression

## Forward Secrecy  [concept_forward_secrecy]  (property; 144 papers)
FECGKA's new init key can improve practical forward secrecy because it can be deleted immediately after a join, even if a leaf-node key is compromised in an early epoch. This chunk's simplified model still exposes all past key packages on compromise and therefore cannot capture that increase.
Papers: 2004_borisov_otr, 2009_danezis_sphinx, 2009_goldberg_mpotr, 2012_backes_provably_secure_onion, 2013_marlinspike_ratcheting, 2013_tor_prop224_rendng, 2013_tox_protocol_spec, 2014_backes_tuc
- assumes: Decisional Diffie-Hellman (DDH); Random oracle functions; ρ μ π primitive security
- compares_with: TreeKEM
- contradicts: Direct-path-only refresh; Recipient compromise exposure; Welcome and leaf key reuse
- defends_against: Compulsion attack
- extends: Message secrecy
- instance_of: Freshness cleanness conditions; Message Key Exchange FmKE; Olm forward secrecy conditions
- measures: Anonymity
- part_of: Post-Compromise Security; Post-compromise forward secrecy (PCFS)
- proves: Standard Model adaptive security loss
- provides: End-to-end encryption; GURKE; Honesty graph; Long-term PIR state risk; Post-Compromise Security; Quantum-vulnerable public-key algorithms; Secure messaging (SM); Tree-based MKA (TMKA)
- requires: Adversary oracle access; Diffie-Hellman key exchange; End-to-end key Kte2e; Ephemeral secret erasure; Epoch key schedule; Message key compromise paths; Secret deletion schedule; Topic access key Ktauth; Traffic analysis excluded from cryptographic claim
- uses: Epoch tracking; Verifiable DH-OPRF

## Private Information Retrieval  [concept_private_information_retrieval]  (protocol; 119 papers)
PIR lets a user query a server database without revealing which information was retrieved. It can store inbox and contact databases; server knowledge of the connecting node is not associated with the protocol messages retrieved, providing recipient and participation anonymity and unlinkability, but no default sender anonymity.
Papers: 1998_chor_pir, 2004_boneh_peks, 2005_ostrovsky_streamingsearch, 2006_ishai_cryptography_from_anonymity, 2010_pfitzmann_terminology, 2013_yoon_adaptation_techniques, 2015_borisov_dp5, 2015_corrigangibbs_riposte
- assumes: Noisy Curve Reconstruction assumption; Server noncollusion assumption; Single-server PIR model
- compares_with: Differential privacy style query leakage; Noise privacy lemma; Offline server transfer; Open technical questions; Secure multiparty aggregation; Single-server full-download bound
- contradicts: Horizontal scalability; Recipient-side indistinguishability
- extends: GC-PSI; Oblivious Transfer; PrivEx aggregate analytics
- implements: Anonymous curve queries; Primary-server PIR aggregation; Write-private database scheme
- improves_on: Setup filter transfer
- instance_of: Offline/online PIR; One-round protocol; Pynchon Gate; Secret-sharing-based ACNs; XOR-based IT-PIR
- measures: Fetched onion addresses; IT-PIR request cost; IT-PIR server computation cost; PIR amortized cost; PIR rate; Published onion addresses; Unique client IP count
- motivates: Distributed Point Function; Query privacy motivation; Riposte complexity comparison
- provides: Baseline PIR linear communication; PIR corruption threshold; PIR receiver privacy; Per-database information-theoretic privacy; Per-server index-independent queries; Privacy properties; Pynchon Gate; Recipient anonymity; Relationship Unobservability; Subscription Confidentiality
- requires: Asymptotic correctness; Consistent PIR snapshots; Non-colluding PIR servers; Non-communicating databases; PIR resource and trust costs; Server scans every database element; Single-database PIR linear work; Single-server computational assumption
- uses: Cuckoo filter; Dummy bucket queries; Oblivious counters; PIR answer precomputation; Probabilistic batch code (PBC); Query-answer model; XOR subset queries; t-server information-theoretic PIR

## Signal Protocol  [concept_signal_protocol]  (protocol; 116 papers)
The text says Signal originally used 3DH, which offered unrestricted offline deniability but no online deniability; it later switched to X3DH, improving forward secrecy but returning to OTR-like deniability. Signal does not provide strong deniability as described here.
Papers: 2004_borisov_otr, 2013_marlinspike_ratcheting, 2015_unger_sok_securemessaging, 2016_bellare_ratcheting, 2016_cohngordon_pcs, 2016_cohngordon_signal, 2016_facebook_secretconversations, 2016_signal_double_ratchet_spec
- assumes: Fully adversarial network; GDH assumption; Honest public-key distribution; KDFs modeled as random oracles; Out-of-band key verification; Side-channel exclusion
- compares_with: Out-of-order message-key storage; Simultaneous session handling; Unanalyzed goals and threats
- contradicts: Signal transcript-consistency gap
- implements: Invocation message encryption and distribution; libp2p
- instance_of: Multi-stage AKE model; Multi-stage key exchange model; Pairwise Signal operations
- part_of: Double Ratchet
- proves: Case 1.1 requires mm-sPRF-ODH; Case 4.2 extra PRF hop; Multi-stage key indistinguishability; Signal core security result
- provides: Asynchronous secure channel; Compromise resilience scenarios; Forward Secrecy; GKE shared secret as chain-key input; Key Indistinguishability; Post-Compromise Security; Post-Compromise Security (PCS); Repudiability; Six message-key properties; Transcript forgeability
- requires: Prekey signatures omitted; Reduction loss
- uses: 3-DH handshake; AES counter mode; AES-256-CBC and HMAC-SHA256; Asymmetric ratchet; Asymmetric ratchet intermediate value; Centralized key-management representative; Client fanout; Diffie–Hellman key agreement; Digital signatures; Double Ratchet

## Sybil Attack  [concept_sybil_attack]  (attack; 109 papers)
An adversary can launch a Sybil guard-discovery attack against any rendezvous-circuit node; its speed increases with the compromised network fraction and decreases with node rotation time. The proposal assumes attacks are observable through large numbers of new nodes, traffic, or test circuits.
Papers: 2002_douceur_sybil, 2003_goel_herbivore, 2010_corrigangibbs_dissent, 2011_timpanaro_i2p, 2012_bitmessage_wiki_changelog, 2012_cao_sybilrank, 2012_elahi_guards, 2012_li_sybilcontrol
- attacks: Anonymous blocklisting; Astraea; Blame protocol; Blockchain; Decentralized online social network; Distributed Hash Table; Diversity-oriented admission control; Guard flag selection; IP Colocation Indicator; Identity distinctness
- compares_with: Eclipse Attack; Onion-service guard discovery attack
- contradicts: Bounded compromised users
- defends_against: IP/subnet graft filtering; Key Privacy; Node admission trust requirement; Proof of Work; Sybil resistance resource requirement; Trace consistency validation; Trusted membership service provider
- implements: Anonymity-set manipulation attack; Attack-edge graph partition; Tor transaction deanonymization
- instance_of: Clustered attacker layout; Covert flash test configuration; Eclipse Attack; Mixed attacker layout; Shadow-relay flag manipulation
- motivates: Censorship attack; Cold boot attack; Eclipse Attack; Flash attack; One-third adversarial-node example; VeraSel
- part_of: Eclipse Attack
- proves: Faulty entity identity capacity
- provides: Consensus weight; Eclipse Attack; Large-scale partition attack
- requires: IPFS 0.4.23 attack
- uses: Address-cookie fingerprinting; Eclipse Attack; Entry-node fingerprinting; First-arrival peer inference; Worst-case identifier flooding

## Post-Compromise Security  [concept_post_compromise_security]  (property; 92 papers)
The theorem supports post-compromise security subject to healing conditions. Add-only commits provide no recovery unless the PSK is unknown to the attacker; signature keys need regular rotation or secure storage, and initialization keys/key packages must not be too old.
Papers: 2013_marlinspike_ratcheting, 2016_cohngordon_pcs, 2016_cohngordon_signal, 2016_matrix_megolm_spec, 2016_signal_double_ratchet_spec, 2017_cohngordon_art, 2017_kobeissi_verification, 2017_rosler_more_is_less
- assumes: Session-state compromise
- compares_with: Perfect Forward Secrecy; TextSecure Version 3 variant analysis
- contradicts: Application-level PCS gap; External commit operation
- defends_against: Device compromise; Server-state compromise
- extends: Double-join prevention; Message secrecy; PSK cross-group healing; Randomness leakage resilience; dom-safe concurrent PCS guarantee
- improves_on: Previous keys in Full Ratchet derivation
- instance_of: Fine-grained PCS; Lack of backward secrecy; Olm post-compromise condition; Session-specific post-compromise security; Sub-optimal PCS
- part_of: Post-compromise forward secrecy (PCFS)
- provides: Anonymity; Double Ratchet; GURKE; Honesty graph; Rotatable Zero Knowledge Set; Secure messaging (SM); Tree-based MKA (TMKA)
- requires: Average update lower bound; Epoch key schedule; Group round-trip; Mandated rekey cadence; PCS healing conditions
- uses: Update proposal

## Mixnet  [concept_mixnet]  (protocol; 101 papers)
Mix networks offer high-latency anonymous communication but are difficult to protect against traffic analysis; many designs are also vulnerable to active disruption. Existing techniques to ensure shuffle randomness in the presence of compromised members require a batch to pass through a series of independent shuffles.
Papers: 2005_camenisch_onion_formal, 2009_danezis_sphinx, 2010_corrigangibbs_dissent, 2010_pfitzmann_terminology, 2012_mulamba_design, 2013_gelernter_limits_provable_anonymity, 2013_kohlweiss_anonymitypke, 2014_bensasson_zerocash
- assumes: One honest mixer; Perfect anonymous channels
- attacks: Flooding attacks; Global active adversary; Malicious mix attacks; Mix collusion; Sender anonymity; Synchronous timeout risk; Traffic Analysis
- compares_with: Mixnet Cost and Latency Concern
- contradicts: Unlinkability with untrusted database
- defends_against: Conditional delivery; Decentralized messaging social-graph leakage; Global network adversary; Network metadata leakage; Network-wide observer; Traffic Analysis
- hides: Broker gateway; Message metadata; Round-based ephemeral dead drops
- implements: Mixer batching; Synchronized mix slots
- improves_on: Onion Routing
- instance_of: Communication relationship
- leaks: Aggregate call-volume upper bounds; Mixnet ciphertext-size cost; Mixnet latency cost; Traffic Analysis
- measures: Average packet latency; Median packet latency; Mixnet latency cost
- motivates: Anonymity Trilemma
- provides: Batched-message delay; Differential Privacy; Global Adversary Goal; Global Observer Protection Claim; High-latency applications; Metadata Privacy; Out-of-band payment notification; Relationship anonymity; Same-timeframe anonymity set; Service Provider
- requires: At least one honest server; Dynamic mix-network scaling challenge; Honest messages per round; MIXes collection limitation; Maximum three mixers; One honest mix server
- uses: Bulletin board; Cover Traffic; Laplace noise messages; Mixer nodes; Mixing; Mixnet Reordering; Re-randomizable encryption; Sphinx; Zero-Knowledge Proof

## Double Ratchet  [concept_double_ratchet]  (protocol; 90 papers)
The asynchronous protocol uses per-message keys within ratchets and tolerates reordered or dropped ciphertexts. Its ciphertexts reveal session and sender through repeated cryptographic values and counters; baseline confidentiality includes forward and post-compromise security.
Papers: 2013_marlinspike_ratcheting, 2015_unger_sok_securemessaging, 2016_cohngordon_pcs, 2016_cohngordon_signal, 2016_matrix_olm_spec, 2016_ncc_olm_review, 2016_signal_double_ratchet_spec, 2017_cohngordon_art
- assumes: Passive adversary
- attacks: TextSecure multi-device impersonation
- compares_with: Continuous Group Key Agreement (CGKA); Dropped messages delay SPQR PCS; Intermediate secret state; Prior RKE protocols weak in new models; Sender Keys; Single group ciphertext
- contradicts: Harvest Now, Decrypt Later Attack
- defends_against: CCA-style attacks after compromise
- extends: Header encryption variant
- implements: Implementation key-retention limit; Ping-pong asymmetric ratchet
- instance_of: Signal Protocol; Stateful key rotation
- measures: Pond adoption
- motivates: Delayed group recovery; Exposure resilience; MLS
- part_of: Secure-messaging scheme SM
- proves: FDR functionality
- provides: Authenticity; Backward secrecy; Confidentiality; Forward Secrecy; Forward secrecy; Future secrecy and recovery; Healing; Immediate decryption; Immediate decryption and message-loss resilience; Integrity
- requires: Authenticated Diffie-Hellman; Initial key exchange functionality; Signal 2000-key window; X3DH
- uses: Asymmetric ratchet; CKA scheme; Continuous key agreement (CKA); Diffie-Hellman ratchet; Forward-secure AEAD (FS-AEAD); KDF chains; Message key derivation; Outbox indexing key chains; Per-message key derivation; Public-key ratchet

## Bloom Filter  [concept_bloom_filter]  (primitive; 90 papers)
The PSPH uses Bloom Filters to improve topic storage and matching. The evaluated configuration expected ten million elements with false-positive probability 0.00001%; initialization made it slower than vectors at first, with the processing-time crossover around 50 topics.
Papers: 2005_ostrovsky_streamingsearch, 2011_giannaki_supporting, 2011_malekpour_endtoend, 2011_mega_dissemination_decentralized, 2011_sanchezmonedero_ddsbloom, 2011_sarela_bloomcasting, 2012_bip37_bloomfilter, 2012_ciobanu_data
- compares_with: BRISA tree and DAG
- contradicts: Full privacy
- defends_against: SPV client privacy loss
- implements: Efficient noise verification; Group instantiation; LIPSIN source routing cost; PSIRP Bloom filter forwarding; Publish/Subscribe
- improves_on: Ciphertext sizes; Dialing bandwidth and latency; Encrypted matching; Forward Secrecy; Linear matching baseline; Per-group router state; Single-retrieval comparison; Storage overhead scaling; Vuvuzela
- instance_of: R-FMD2; Routing information sketches
- leaks: Bloom filter leakage; Bloom-filter false positive; Bloom-filter false positives; Containment graph inference; Filter debugging limitation; Partial URL hash leakage; Response time; Server database privacy goal; Topic filtering for scalability; iBF false positives
- measures: False positive experiment; Guessing privacy metric; Publisher state memory example; Subscription response reduction; Subset-test false-positive example
- motivates: Bloom false-positive forwarding anomalies; False-positive causes; Flow duplication; Forwarding loops; Packet storm; δ-Onion-Correctness
- part_of: CRLite enumeration limitation
- provides: Anonymity Set; Benchmark confidence intervals; Bloom Filter False Positive; Bloom filter false positive rate; Bloom filter false positives; False Positive Rate Formula; False-positive sources; Filter sizing parameters; Set-equality false positive bound; Shard size
- requires: Candidate-set refinement; Estimated maximum tag-set size; Filter Rebuild on Deletion; Pseudorandom onion ciphertexts; Subscription data model
- uses: Private Information Retrieval; Topic-based Bloom Filter matching

## Onion Routing  [concept_onion_routing]  (protocol; 96 papers)
A source-rewriting system in which the sender chooses a full route and encrypts packets in layers; each forwarding node reorders packets, removes one encryption layer, and forwards them. The paper says such systems do not provide strong anonymity against passive traffic analysis.
Papers: 2003_goel_herbivore, 2005_camenisch_onion_formal, 2011_pace_gossiping, 2011_timpanaro_i2p, 2012_backes_provably_secure_onion, 2012_elahi_guards, 2012_feigenbaum_onion_blackbox, 2012_mulamba_design
- assumes: Adversarial link delivery
- attacks: Entry short-term key compromise; Global traffic analysis; Traffic Analysis
- compares_with: Mixnet; Source-routed layered mixnet; Supported topologies; Tor; Unlinkability with untrusted database
- contradicts: Global network adversary; Onion routing traffic-analysis limitation
- defends_against: Conditional delivery; Local passive adversary; Locator identity leakage; Traffic Analysis
- extends: Repliable onion encryption; Tor; Tor bandwidth-weighted selection
- hides: Broker gateway; Local passive WF adversary; Metadata Privacy; Sender-Receiver Unlinkability
- implements: Layered packet encryption; Mixnet; Per-hop knowledge limits
- instance_of: Mixnet; Tor; UC ideal onion-routing functionality
- leaks: Corrupt-node onion leakage; Network adversary; Traffic Analysis; Traffic correlation by circuit seniority
- measures: Video quality by link capacity
- part_of: Tor
- provides: Anonymity; Anonymity Set; Anonymous channel functionality; Black-box functionality; Privacy properties; Recipient anonymity goal; Request confidentiality; Sender anonymity goal; Sender-Receiver Unlinkability; Strong anonymity guarantees
- requires: At least one honest relay; Encrypted sendback data; Maximum onion path length; Maximum path length N; Random 24-byte nonces
- uses: Dummy Messages; End-to-end circuit keys; Fixed-size IP_Port encoding; Idealized encryption; Mix-node; Rendezvous Point; Temporary per-path public keys; Three-node circuit; Three-router circuit; Universal composability (UC) framework

## Content-Based Pub/Sub  [concept_content_based_pub_sub]  (protocol; 88 papers)
Filters are evaluated against event content, with subscribers specifying predicates that range from comparisons and Boolean combinations to regular expressions or XPath expressions. This is described as the most general scheme supported by systems such as Hermes and JEDI.
Papers: 2011_carzaniga_contentbased, 2011_guidec_communicationbasee, 2011_hosoda_approximability_minimum, 2011_konstantinidis_content, 2011_malekpour_endtoend, 2011_sarela_bloomcasting, 2011_tajuddin_techniques, 2012_chaabane_ontology
- compares_with: Naive Matching Heuristic; Topic model mobile tradeoff; Topic-Based Pub/Sub; Topic-Connected Overlay; Topic-based identifiers
- extends: Hybrid topic and content filtering
- implements: Publish/Subscribe; Ranked data dissemination; Siena Fast Forwarding matching framework
- improves_on: Broker-node scaling issue
- instance_of: CCN Interest and Data; Publish/Subscribe
- motivates: Content overlay design steps; Sequence gaps from filtering; Soft-link adaptive overlay
- part_of: Publish/Subscribe
- provides: Content-selected recipients; Eight spatial relational operators; Eight topological relations; Event correlation; Event retention; Filter predicate; Publisher-recipient decoupling; Range Value Matching; Selective destination sets; Subscription delivery tree
- requires: Design-time configuration assumption; Exponential logical topics; Filtering overhead and expressiveness trade-off; Interest Profile; Known attribute domains and granularity; Simulator limits optimization to channels; TCO content-based limitation
- uses: 2D Region; Bloom Filter; Broadcast-all baseline; Broker Subscription Routing; Broker overlay; Broker overlay graph; Content predicate subscriptions; DHT rendezvous routing; Directional Random Walk (DRW); Distributed Hash Table

## MLS  [concept_mls]  (protocol; 58 papers)
Messaging Layer Security provides forward secrecy and post-compromise security and is designed for large groups, but requires group-state messages to be processed in one total order. Updates and membership changes use O(log n) broadcast size; a semi-trusted service typically determines commit order.
Papers: 2017_cohngordon_art, 2018_bhargavan_treekem, 2019_bhargavan_mls_formal, 2020_alwen_mls_insider, 2020_bienstock_group_ratcheting_concurrency, 2020_weidner_decentralized_sgm, 2021_alwen_key_grafting, 2021_alwen_server_aided_cgka
- assumes: Authentication Service (AS); Complete public tree view; Delivery Service (DS); Ordered group broadcast channel; Trusted Authentication Service
- attacks: Modified PKE ciphertext attack
- compares_with: Delayed tree refresh upper bound; Sender Keys
- contradicts: Decentralized network requirement; Post-Compromise Security; Two-party scope
- defends_against: Dynamic membership double-join risk
- improves_on: Shared group-key security limits
- instance_of: ITK; TreeKEM
- leaks: Dynamic access-pattern metadata; Static explicit metadata
- motivates: Dynamic membership operations; Threshold authorization for device management
- part_of: TreeDEM; TreeKEM; TreeSync
- proves: Single-epoch key schedule security (Lemma 3)
- provides: Continuous group authenticated key exchange; Forward Secrecy; Forward secrecy (FS); Key freshness chaining; MLS modular decomposition; MLS update overhead O(log n); Membership authentication; Post-Compromise Security; PrivateMessage; PublicMessage
- requires: Hybrid KEM; KDF; Sequential update restriction; XPD
- uses: Central server verification; Cipher-suite primitives; Continuous Group Key Agreement (CGKA); Continuous Group Key Derivation (CGKD); Credential identity binding; Delivery Service (DS); Filtered direct path; Group message authentication; Labeled HPKE encryption; Labeled signatures

## GossipSub  [concept_gossipsub]  (protocol; 50 papers)
Prior work modeled Gossipsub in ACL2 S and found counterexamples showing that certain Ethereum configurations allow Sybil nodes to violate scoring safety properties, causing large-scale partition or eclipse attacks. The authors aim to refine Floodnet toward a specification close to Gossipsub.
Papers: 2019_vyzovitis_gossipsub_v01, 2020_cortes_eth2_p2p, 2020_gossipsub_v11_spec, 2020_leastauthority_gossipsub_audit, 2020_savolainen_streamr_network, 2020_vac_waku2_relay_spec, 2020_vac_waku2_spec, 2020_vyzovitis_gossipsub
- assumes: Unstructured peers and churn
- attacks: Cold boot attack; Covert flash attack; Degradation attack; Single-target censor attack
- compares_with: Attack at dawn delivery rate; Covert flash delivery rate; Distributed Hash Table; IP collocation delivery rate; PolderCast; Proof of Stake; Rappel; Scribe; Vitis
- defends_against: Peer-sampling eclipse attack
- extends: Floodsub
- implements: Gossip control messages
- improves_on: Content-based matching cost
- instance_of: Publish/Subscribe; Topic-Based Pub/Sub
- leaks: Metadata Privacy
- measures: Attack at dawn latency; Covert flash latency; IP collocation latency; Message learning and peer score asymmetry; Publisher eclipse delivery result; Publisher eclipse test setup
- motivates: Millions-node scale target
- part_of: Specification consolidation recommendation
- provides: Bounded degree and amplification; Peer Exchange bootstrap; Peer scoring spam protection; v1.1 more resistant than v1.0
- requires: Ambient peer discovery; Security evaluation deferred
- uses: Adaptive gossip dissemination; Eager push mesh; Explicit peering agreements; Flood publishing; Flood-publish mitigation; Gossip message metadata; GossipSub peer pruning; Heartbeat; Higher precision latency simulation model; Lazy gossip pull

## Zero-Knowledge Proof  [concept_zero_knowledge_proof]  (primitive; 78 papers)
The proof system proves a statement from primary and auxiliary inputs without revealing auxiliary information beyond what the statement implies. Zcash uses preprocessing zk-SNARKs, with completeness, knowledge soundness, and statistical zero knowledge required with overwhelming probability for generated keys.
Papers: 2010_pfitzmann_terminology, 2013_corrigangibbs_verdict, 2013_vansaberhagen_cryptonote, 2014_chase_algebraicmacs, 2014_franck_dc_collision_resolution, 2014_frosch_textsecure_analysis, 2015_corrigangibbs_riposte, 2015_decouchant_collusions
- assumes: DDH assumption
- defends_against: Bayer-Groth verifiable shuffle; Compromised moderation infrastructure; Insider splitting attack; Megolm unknown key-share attack; Threshold unforgeability
- extends: Polynomial commitment scheme (PCS)
- hides: Minimal disclosure claim; Proof fields attached to messages; Shielded transactions; Showing discloses selected attributes
- implements: Fiat-Shamir heuristic; Payment consistency proof; Per-message RLN proof
- instance_of: SNARK; zk-SNARK
- measures: General-purpose ZKP overhead
- proves: Coin matching lemma; Insignificant soundness error; Negligible anonymity advantage; Nullifier; Reversible point-addition circuit; Structured transaction identifier
- provides: Application message structure checks; Client ciphertext anonymity; Credential anonymity; Cross-chain messaging; Interaction privacy; Issuer identity privacy; One-time output keys; Outstanding UTXO anonymity set; Signer anonymity with early key exposure; Withholding attack-circuit details
- requires: Credential presentation; HKDF public key derivation; Knowledge soundness; Round-bound authentication key; Unique nonce lemma; Unpredictable gossip inputs; ZK nonmalleability omitted
- uses: Dual Mode DCN; Fiat–Shamir transform; Pedersen commitment; Yang et al. quadratic-relation framework

## Distributed Hash Table  [concept_distributed_hash_table]  (primitive; 81 papers)
A standard abstraction with put(key,value) and get(key) operations for storing and fetching data by key. First-generation DHTs use consistent hashing to map keys and values to nodes, remapping only a fraction of keys as peers join or leave and balancing load uniformly with high probability.
Papers: 2011_chen_scaling_construction, 2011_sarela_bloomcasting, 2012_baldoni_dynamic_message, 2012_chaabane_ontology, 2012_ferretti_publish_subscribe, 2012_li_sybilcontrol, 2012_matos_brisa_combining, 2013_buford_applicationlayer
- attacks: Eclipse Attack
- compares_with: Content-Based Pub/Sub; E-StreamHub fixed slices; Gossip recommendation systems; IoT device computation limitation; Pastry DHT; Reservation key prefix; Topic-Connected Overlay; Viceroy and Koorde routing bound
- contradicts: DHT exact matching limitation
- defends_against: Churn
- implements: Content-based routing; DHT event matching and rendezvous; Kademlia; Meghdoot storage and latency tradeoff; Onion descriptor placement; Veilid DHT storage
- improves_on: DHT query privacy extensions; One-hop routing
- instance_of: Chord; Kademlia; Pastry DHT
- leaks: DHT hashing destroys locality; Passive network-pattern observation
- measures: DHT lookup latency tradeoff
- provides: ALMTree DHT Storage; Chord lookup; DHT fault tolerance and scalability; DHT lookup scale; Eventually consistent hub state; Kademlia; Pastry lookup; Publish/Subscribe; Semantic-free indexing exact-match limit; Structured overlay properties
- requires: DHT maintenance overhead; I2P
- uses: 160-bit DHT keyspace example; Commensal cuckoo rule (CCR); Consistent hashing; Cuckoo rule (CR); Fully peer-to-peer network; Query Privacy protocols (QP); Rendezvous routing; Robust Communication Protocols (RCP); Scribe; Sync ID

## Eclipse Attack  [concept_eclipse_attack]  (attack; 62 papers)
Byzantine nodes can bias dissemination by overrepresenting their own identifiers in gossip, gradually poisoning correct nodes’ views and enabling eclipse attacks and higher-level protocol manipulation. Concrete Bitcoin attacks demonstrate feasibility and impact.
Papers: 2011_pace_gossiping, 2013_boutet_decentralizing, 2013_mega_social_overlays, 2014_biryukov_deanonymisation, 2015_heilman_eclipse, 2016_chen_overlay_design, 2016_neudecker_timing, 2017_apostolaki_hijacking
- assumes: Byzantine fault model
- attacks: Bitcoin P2P network; Connection slots; Countermeasure trade-off; Cut detection guarantee; Ethereum; FireSpam; Inhibiting messages through peer eclipse; Monero; PANDAS; Peer notification brokers
- compares_with: Attacker connection requirement; Attrition defenses; Hub and eclipse attack orthogonality; ProxyMark attack requirements
- extends: Encrypted communication
- instance_of: Attack at dawn test configuration; Byzantine view poisoning; Eclipse-attack experiment; Location exploitation; Multistage Ethereum eclipse attack; Profile-mirroring censorship attack; Sybil Attack; Topology knowledge enables attacks; Tor exit banning
- measures: Attack 7 full eclipse time; Attack 7 occupation time; Eclipse demonstrated; Fastest full eclipse; Slowest outgoing connection occupation
- motivates: Block propagation fork risk; Sybil Attack
- proves: IPFS eclipse outcome
- provides: Adversarial forwarding failure; Mining and consensus impacts; Zero-confirmation double spend
- requires: Address-table seeding; Eclipse connection maintenance; Sybil Attack
- uses: Abstract P2P attack model; Ciphertext replay; PING/PONG payload choice; Sybil Attack; TCP payload replay; Timing-based topology inference

## X3DH  [concept_x3dh]  (protocol; 61 papers)
Swarm uses X3DH for initial contact and to establish a shared secret that seeds post-handshake encryption. The implementation uses secp256k elliptic curve, Keccak256, and 64-byte EC public-key encoding; one-time pre-keys are omitted because replay protection is handled elsewhere.
Papers: 2016_cohngordon_signal, 2016_signal_x3dh_spec, 2017_cohngordon_art, 2017_rosler_more_is_less, 2017_signal_sesame_spec, 2018_alwen_double_ratchet, 2018_status_whisper_usage_spec, 2018_unger_deniable
- assumes: Deniability; K2DH parameters; gapDH
- compares_with: Asynchronous DAKE construction; Cross-protocol KDF confusion; Signal-conforming AKE
- extends: 3DH; Double Ratchet; Static-static DH extension
- implements: X3DH key agreement computations
- measures: Initial DH computation
- motivates: XZDH
- part_of: Initial key-generation model gap; Signal Protocol
- proves: Deniability theorem bound; Non-constructive simulator; Responder deniability for X3DH and PQXDH
- provides: Asynchronous exchange; Asynchronous initiation; Asynchronous messaging; Asynchronous setup; Deniability; Double Ratchet; Forward Secrecy; Receiver obliviousness; Session key; Signal master secret
- requires: Extended Knowledge of DH assumption; HKDF derivation; Prekey bundle; Protocol participation assumptions; Public-key infrastructure assumption; QR pairing channel; Random-oracle KDF; X3DH public-key bundle
- uses: Asynchronous prekey setup; Central server; Contact-code topic; Double Ratchet; ECDSA; ECIES; HKDF and HMAC-SHA256; Keccak-256; Keccak256; One-time prekey deletion

## TreeKEM  [concept_treekem]  (protocol; 40 papers)
The (R)TreeKEM CGKA protocol uses a left-balanced binary ratchet tree with members at leaves and PKE key pairs at all nodes except the root. Each member knows secret keys on its direct path; an update creates fresh key pairs on that path and encrypts information for each co-path subtree so members can derive the new root update secret.
Papers: 2018_bhargavan_treekem, 2019_alwen_tainted_treekem, 2019_bhargavan_mls_formal, 2020_alwen_mls_insider, 2020_bienstock_group_ratcheting_concurrency, 2020_weidner_decentralized_sgm, 2021_alwen_key_grafting, 2021_alwen_server_aided_cgka
- assumes: Uniform committer assumption
- attacks: Concurrent TreeKEM degradation; Tree update verification issue
- compares_with: Asynchronous Ratcheting Trees (ART); DeCAF; Explicit proposal sorting; TreeKEM expansion cost overhead
- defends_against: Dynamic membership double-join risk
- extends: multi-KEM (mKEM)
- implements: Co-child path encryption; Commit; MLS; Node encapsulation functions; Tree epoch update; Tree path refresh
- improves_on: Asynchronous Ratcheting Trees (ART); Lower recipient computation than ART; TreeKEM receiver cost
- instance_of: Continuous Group Key Agreement (CGKA); Offline publicly-computable update cost; Weak CGKD (wCGKD)
- leaks: Sender Anonymity
- measures: Add and remove operation cost; Create operation cost; Four-user ratchet-tree update example; McEliece mobile-plan depletion; Per-group local state storage; TreeKEM commit encryption count; TreeKEM handshake complexity; Update communication cost; Update operation cost; rTreeKEM communication saving
- part_of: MLS
- provides: Concurrent operation merging; Deterministic add location; Forward Secrecy; Member addition; Member removal; Message integrity; Message secrecy; Post-Compromise Security; TreeKEM logarithmic commit cost; TreeKEM per-user commit cost
- requires: Collision-resistant hash function; Group operation ordering; Tree integrity invariant; Tree secrecy invariant; Untrusted asynchronous delivery server
- uses: Authenticated Encryption; Confirmation tag; Hybrid public key encryption; Key Encapsulation Mechanism; Left-balanced binary subgroup tree; Pseudo Random Function; Ratchet Tree; Ratchet tree; Tree-Based Group State; Tree-based group keys

## Anonymity Set  [concept_anonymity_set]  (property; 70 papers)
SUMS and RUMS can provide recipients an anonymity set of all registered clients with mailboxes, if clients follow the described mailbox or per-round retrieval behavior. In RUS or SUBS, adversarial manipulation can reduce the effective set to a victim.
Papers: 2010_corrigangibbs_dissent, 2010_pfitzmann_terminology, 2011_sanchezmonedero_ddsbloom, 2013_ciancaglini_keybased, 2013_corrigangibbs_verdict, 2013_oya_sda_family, 2013_vansaberhagen_cryptonote, 2014_biryukov_deanonymisation
- attacks: Long-term intersection attack
- compares_with: Limited mixing comparison
- defends_against: Provider message-count leak
- hides: Publish/Subscribe
- improves_on: Horizontal Scaling
- instance_of: Global message shuffle
- measures: Back’s Linkable Spontaneous Anonymous Group (bLSAG); Table 1 entropy values
- motivates: Small and dynamic site recommendation
- part_of: Tor
- provides: Anonymity; PPUSTMAN architecture; Path entropy limitation; Sender Unobservability
- requires: Attacker perspective; Cover Traffic; Reidentifying claims; Shortest common supersequence defense
- uses: Cover Traffic; Distributed Hash Table

## Sphinx  [concept_sphinx]  (protocol; 44 papers)
An efficient onion packet format with a header containing routing information and temporary keys protected by per-hop MACs, plus an encrypted payload. In the integrated system model, a corrupted first relay can tag the payload and a collaborating receiver can identify the sender relationship.
Papers: 2009_danezis_sphinx, 2016_gelernter_anonpop, 2017_piotrowska_annotify, 2017_piotrowska_loopix, 2017_ruffing_p2p, 2018_chen_taranet, 2018_degabriele_untagging_tor, 2019_burgel_hopr
- assumes: Decisional Diffie–Hellman assumption; Random oracle model
- attacks: Reply traceability
- compares_with: Active global adversary; CL05 format; Denial of service attack; Minx; Mixmaster; Mixminion; Möller format; SSH08
- contradicts: Throughput estimate
- defends_against: Active tagging attack; Replay attack; Tagging attack; Traffic Analysis
- hides: Path length hidden; Relay position hidden
- implements: Onion Routing
- improves_on: Hybrid onion encryption; Mixminion
- instance_of: Mixnet
- leaks: Sphinx path length leak
- measures: Per-message processing cost; Relay processing cost; Sender packet construction cost; Sphinx ECC overhead at five hops; Sphinx RSA overhead at five hops
- part_of: Sphinx padding flaw
- proves: Integrity path bound; Reduction-based security guarantees; Universal composability result
- provides: Bitwise unlinkability; Forward Secrecy; Forward/reply indistinguishability; Message indistinguishability; Mix strategy flexibility; Packet overhead; Payload integrity gap; Payload tampering destruction; Reference implementation size; Replay detection tag
- requires: Maximum path length; Maximum path length N; Public-key infrastructure; Security parameter; Single honest mix condition
- uses: Curve25519; Diffie-Hellman; Encrypt-then-MAC; LIONESS; Message padding; Onion-Security; Per-hop Diffie–Hellman keys; Reply-block state; Seen-message tag table

## Topic-Connected Overlay  [concept_topic_connected_overlay]  (system; 61 papers)
Hosts form an overlay and use unicast connections between pairs of hosts for dissemination; hosts handle group management, routing, and tree construction without Internet-router support. The design uses one shared overlay for multiple multicast sessions.
Papers: 2011_hosoda_approximability_minimum, 2011_mega_dissemination_decentralized, 2011_pace_gossiping, 2011_sarela_bloomcasting, 2011_tajuddin_techniques, 2012_chen_generalized_algorithm, 2012_matos_brisa_combining, 2012_setty_poldercast
- compares_with: Content-Based Pub/Sub; Minimal-broker allocation NP-hardness; Pull-only propagation; Push-only propagation
- contradicts: TCO content-based limitation
- defends_against: Scribe unwanted traffic
- extends: Partial TCO; Structured overlays; Unstructured overlays
- implements: Downstream replication; MU DEBS; One-hop clustering; Upstream evaluation
- improves_on: Overlay latency; Overlay link costs; Pure forwarding overhead
- instance_of: DPS interest tree; Min-TCO LOGAPX-completeness; Publish/Subscribe; Selective filtering; Topic-Based Pub/Sub
- motivates: Pure forwarding; Trusted-user sharing condition
- part_of: Publish/Subscribe
- provides: Bounded topics per user hardness; Bounded users per topic results; Broker Overlay Network; Dependability guarantee; Open topic-count range; Polynomial-time topic threshold; Publish/Subscribe; Routing resource savings; TCO routing cost savings; TCO routing savings
- requires: Bounded node degree; Dynamic Interest Patterns; Induced topic subgraph; Local-view size; Overlay density tradeoff; Rendezvous Point; Topic-connected component
- uses: Bounded membership views; GM heuristic; Local-view entry; Parametric subscriptions; Peer selection variants; Push-pull view propagation; Shuffle length; Shuffling period; View selection strategies

## DC-net  [concept_dc_net]  (mechanism; 61 papers)
DC-Net uses secret sharing and XOR-based decryption in rounds where only one node may send; collisions prevent delivery. Breaking anonymity requires controlling every node, but each round requires every node pair to exchange messages, making communication and computation expensive; considered unusable above 50 peers in practice.
Papers: 2003_goel_herbivore, 2010_corrigangibbs_dissent, 2010_pfitzmann_terminology, 2012_wolinsky_dissentnumbers, 2013_corrigangibbs_verdict, 2013_gelernter_limits_provable_anonymity, 2013_wolinsky_hang, 2014_movahedi_secure_anonymous_broadcast
- assumes: DCnet trust assumptions
- attacks: Collision jamming; DC-net collision denial of service; DC-net collisions; DC-net jamming attack; DCnet anonymous denial of service; DCnet collisions; DoS attacks; Sybil Attack; Synchronous timeout risk
- compares_with: Crowds degree-of-anonymity levels; Group arithmetic computation cost; Mis-authenticated upload attack; Pung; Pung user scale claim; Three-server Riposte
- contradicts: DC-net lacks t-liveness; Privacy and anonymity performance cost; Sender anonymity
- defends_against: Traffic Analysis
- extends: Dissent
- hides: Veto count privacy
- implements: DiceMix; Dissent; Verdict
- improves_on: Dissent; Untraceable VoIP protocol
- instance_of: Communication relationship; Dissent; Feasible relaxed anonymity definition; Multicast/broadcast anonymity; Secret Sharing; Verdict
- leaks: Traffic Analysis
- measures: DC-Net scale limit; DC-net communication overhead; Typical DC-Net cost
- proves: Veto detection probability
- provides: Anonymity Set; Bandwidth overhead B; DC-net round costs; Information-theoretic anonymity; One message per DC-net round; Privacy properties; Publish/Subscribe; Relationship anonymity; Relaxed ultimate anonymity; Sender anonymity
- requires: DC-net network cost; DCnet participation requirements; Honest-user setting
- uses: Cryptographic PRNG; DC-net cryptographic scheduling; Diffie–Hellman key agreement; Ephemeral-key recipient anonymity; Noise messages; Pairwise symmetric keys; XOR

## MQTT  [concept_mqtt]  (protocol; 62 papers)
MQTT supports many-to-many IoT communication and three QoS levels, but the chunk says it lacks strong authentication or authorization and has difficulty integrating delegated OAuth. Prior comparisons report better reliability than CoAP at high request frequency, while CoAP uses less bandwidth and has lower round-trip time.
Papers: 2011_davis_presencearchitecture, 2013_morales_hottopic, 2014_dominguez_contribution, 2015_chen_weighted_overlay, 2016_siegemund_psvr, 2017_bouloukakis_timelinessintermittent, 2018_anon_publishsubscribe, 2018_benson_firedexprioritized
- assumes: Central broker failure
- attacks: Denial of service attack
- compares_with: CoAP; DDS bandwidth versus MQTT; Ordered exactly-once delivery; ROS 2 middleware (RMW) comparison; Reported delay reduction; Reported network usage reduction
- contradicts: MQTT real-time limitation
- extends: MQTT 3.1 connection extension; MQTT-S; MQTT-SN; Three-level MQTT security framework
- implements: Broker containers; Forward collision warning application; Publish/Subscribe; Topic-Based Pub/Sub; UCONABC
- instance_of: Centralized broker bandwidth and failure costs; Cloud-edge messaging model; Publish/Subscribe; Topic-Based Pub/Sub
- leaks: Central broker queuing delay
- measures: 100 message comparison; 100,000 message comparison; Multi-machine latency results; Multi-machine throughput results; Single-machine Kafka and MQTT limits; Single-machine latency results
- motivates: Single broker bottleneck
- provides: MQTT QoS levels; MQTT and CoAP suitability; MQTT header size; Packet size ordering; Protocol choice recommendations; Publish/Subscribe; QoS; QoS 0 best effort; QoS 1 at least once; QoS 2 exactly once
- requires: MQTT broker; MQTT broker bottleneck
- uses: Broker-relay topology; EMQ broker; Ethereum; Hierarchical broker roles; MQTT QoS 1 delivery; MQTT QoS 2 exchange cost; MQTT TCP/IP transport; MQTT TLS ports; MQTT benchmark settings; MQTT broker

## Metadata Privacy  [concept_metadata_privacy]  (property; 57 papers)
The survey identifies confidentiality, ownership privacy, social interaction privacy, and activity privacy as OSN privacy requirements. Social interaction privacy means users can hide interaction patterns; activity privacy prevents application interactions from being exposed publicly.
Papers: 2004_borisov_otr, 2012_libert_anonymousbe, 2014_roos_measuring_freenet, 2016_hopwood_zcash_protocol_spec, 2016_lazar_alpenhorn, 2016_lerner_rangzen, 2016_luo_mpenc, 2016_ncc_ricochet_audit
- assumes: Full network surveillance
- attacks: Traffic Analysis
- defends_against: Network ossification; Traffic Analysis
- extends: Key Privacy
- hides: Ciphertext set linkability; Communication metadata
- leaks: Ephemeral Peer IDs; First-Spy Estimator; Public message content; RSSI proximity information; Session recovered metadata records
- motivates: DDoS attack; Time-bandit attack
- proves: ANO-IND-CCA security
- provides: Balanced transaction privacy; Metadata-private messaging
- requires: At least one honest server

## Proof of Work  [concept_proof_of_work]  (primitive; 65 papers)
Bitmessage uses proof-of-work as an anti-spam measure, requiring an average of four minutes and wasting energy. Bitmessage Plus still uses proof-of-work for address registration to resist Sybil attacks, with target adjusted for constant registration time.
Papers: 2002_back_hashcash, 2004_laurie_proofofwork, 2006_liu_pow, 2012_bitmessage_wiki_faq, 2013_vansaberhagen_cryptonote, 2014_biryukov_deanonymisation, 2015_dziembowski_proofsofspace, 2015_heilman_eclipse
- assumes: Mining and consensus impacts
- attacks: Grover’s algorithm
- compares_with: Hashcash; Identifier pre-generation; MoneyMorph blockchain channel; WAKU-RLN-RELAY
- contradicts: Adoption properties; Gossip scalability limits; Membership-based Sybil resistance
- defends_against: Asynchronous routing; Bulk-message spam; Connection-wide message propagation; Cost-free key-pair generation; Denial of service attack; Gossip flooding; Sybil Attack
- implements: Connection proof of work; Proof-of-work spam defense; SHA512 PoW construction; Server challenge spam guard
- improves_on: Uniform work cost conflict
- instance_of: Almost-uniform key mixing; Bitcoin PoW parameters; Consensus Protocol; Pluggable DoS protection framework
- measures: Five-second PoW example; Random address
- motivates: Offline receiver rebroadcast cost; Secure random peer sampling
- provides: Difficulty measure; Leading-zero-bit difficulty; On-spend public-key window; Sender work cost; Spam deterrence
- requires: Block nonce size; Connection-wide message propagation
- uses: Difficulty filter; Email hash puzzle; Legacy PoW target

## ML-KEM  [concept_ml_kem]  (primitive; 47 papers)
ML-KEM is described as IND-CCA2 secure against quantum adversaries making classical and superposition queries, assuming D-MLWE is intractable and G, H, J are random functions. Public-key/ciphertext/shared-secret sizes are 800/768/32 bytes for ML-KEM-512, 1,184/1,088/32 for -768, and 1,568/1,568/32 for -1024.
Papers: 2016_signal_double_ratchet_spec, 2019_stebila_rfc9954_hybridtls, 2021_simplex_agent_protocol, 2022_maram_pq_anonymity_kyber, 2023_cremers_keeping_up_kems, 2023_kret_pqxdh_blog, 2023_pu_fuzzystealthsigs, 2024_apple_pq3
- assumes: LEAK+r-BIND-SS-{CT,PK} binding; Module Learning With Errors assumption; Module-LWE
- attacks: MAL-BIND-K-PK attack
- compares_with: Ciphertext second preimage resistance (C2PRI)
- contradicts: Binding implication chain
- extends: CRYSTALS-KYBER
- implements: Cached public-key hash; Continuous Key Agreement (CKA); KEM key establishment flow; ML-KEM Braid; ML-KEM shared-secret establishment
- instance_of: Classical and PQ communication ratios; Encryption ratio λ; Hybrid KEM; ML-KEM hash structure; ML-KEM parameter sets; Post-quantum asymmetric cryptographic algorithm
- measures: KEM benchmark results; PQC KEM timings
- motivates: PQC overhead estimate; Post-quantum ternary recommendation
- provides: Ciphertext Second Preimage Resistance; Ciphertext second preimage resistance (C2PRI); Correctness Overwhelming Probability; IND-CCA; KEM binding property; KEM public-key reuse constraints; LEAK+r KEM binding; LEAK+r-BIND-SS-{CT,PK} binding; ML-KEM 768 key and ciphertext sizes; ML-KEM parameter sets
- requires: Approved Randomness Strength; Both components need weak anonymity; Fresh encapsulation randomness; Input Checking; Intermediate Value Destruction; Internal Function Access; ML-KEM input checks; ML-KEM wrapper requirement; No Floating Point Arithmetic; Obfuscated Key Exchange (OKEX)
- uses: Byte Encoding; Centered Binomial Sampling; Compression Decompression; Decrypt and re-encrypt check; Fujisaki–Okamoto transform; Implicit rejection; K-PKE; Number Theoretic Transform; SHA3; SampleNTT

## Ethereum  [concept_ethereum]  (system; 61 papers)
Ethereum is a global distributed computer with accounts, smart contracts, and proof-of-stake consensus. It produces blocks in deterministic 12-second slots, processes most transactions in under a minute, and has private mempools including TEE-based BuilderNet; the text says this makes early fast-clock CRQC on-spend attacks unlikely and offers a mitigation.
Papers: 2015_hakiri_publishsubscribe, 2015_heilman_eclipse, 2015_khare_reactivestream, 2015_tegueu_ddssymbioses, 2017_hayun_optimasipemilihan, 2018_marcus_ethereumeclipse, 2018_ramachandran_trinity, 2019_burgel_hopr
- assumes: Ethereum mostly-honest assumption
- compares_with: δ-delay ledger
- extends: SROS2
- implements: Topic-Based Pub/Sub
- instance_of: BPAC mechanism; Blockchain; Data owners O; Distributed Hash Table; Leakage function Λ; Publish/Subscribe
- motivates: Network-level identity linkability
- provides: Block component sizes; Ethereum encoding capacity; Geth peer connection slots; Keyed DDS instances; Participant pseudonymity; Randomness generation latency; Smart Contract
- requires: DDS QoS mapping; Ethereum funding and call costs
- uses: Data Availability Sampling; Discovery v5.1 (dv5); Distributed Hash Table; ECDSA node identity; Etherdelta contract prevalence; Ethereum topic-advertisement node discovery; GossipSub; IPv6 destination header encoding; Kademlia; Persistent account model

## Anonymity Trilemma  [concept_anonymity_trilemma]  (system; 66 papers)
The user unlinkability game asks whether a target message can be linked to one of two senders after arrival at recipient R. The global passive attacker statically corrupts at most fraction c of mix nodes and controls all other users except the two challenge users.
Papers: 2012_matos_brisa_combining, 2012_naicken_finding, 2013_kazemzadeh_overlay, 2014_fischer_qualityofserviceaware, 2015_abdennadher_gestionqualite, 2015_krasnova_footprint, 2015_unger_sok_securemessaging, 2016_gelernter_anonpop
- assumes: Anonymity bound assumptions; Direct Bluetooth handshake; End-to-end latency equation
- compares_with: Metadata Privacy; Reliable sender and receiver unobservability; Tree-Myco; Waku
- contradicts: Strong anonymity
- instance_of: Publish/Subscribe; Source and destination privacy
- measures: Discrete-event mix network simulator
- motivates: Cover Routing Generation (CRG); Cover traffic cost; Latency tradeoff; Partition lifecycle and recovery; Strong anonymity; Traffic Analysis; Waku v2 Dandelion
- provides: Mixing delay μ; Strong anonymity constraints; Unlinked multiset output
- requires: Bandwidth overhead; Batch mix; Decoy traffic; Expensive cryptographic escape; Latency overhead; Message frequency and patterns; Mixing latency; Traffic Analysis

## Cover Traffic  [concept_cover_traffic]  (primitive; 55 papers)
Nym sends indistinguishable loop packets when no real packet is ready and also sends additional loop traffic continuously at average inter-packet delay λC=200 ms. This hides whether an endpoint is sending application-level traffic from an observer on the endpoint-gateway link.
Papers: 2013_wolinsky_hang, 2015_unger_sok_securemessaging_tr, 2015_vandenhooff_vuvuzela, 2016_angel_pung_1, 2016_gelernter_anonpop, 2016_lazar_alpenhorn, 2017_halpin_nextleap, 2017_overdorf_onion
- contradicts: Metadata obscuring limitation; MixFlow; Mixnet
- defends_against: Application-message confidentiality; Flow matching; Global passive adversary (GPA); Intersection attack; Persistent pattern disclosure; Provider message-count leak; Targeted dropping attack; Traffic Analysis; Traffic correlation attack; Website fingerprinting
- hides: ISP-grade network monitor; Queue message delivery format; Test-packet identification
- implements: Noise requests; Truncated Laplace count noise
- improves_on: Anonymity Set; Entropy; RUS
- measures: Attack accuracy; Detection rate; Tenfold cover-traffic result
- motivates: Failure probability privacy speed relation
- provides: Activity-independent cover traffic; Constant cover traffic; Cover traffic cost; Reliable sender and receiver unobservability; Scale can lower latency and cover traffic; Theorem 2 link probabilities
- requires: Adaptive detection precision
- uses: Phantom channels; Poisson Process

## Dissent  [concept_dissent]  (protocol; 44 papers)
A DC-net system with setup and blame phases that detects disruption after the fact; its blame protocol is quadratic in total users and may run once per malicious user. The chunk reports Dissent measurements with and without blame and that its code hung above 1,000 users or 10 kB messages.
Papers: 2010_corrigangibbs_dissent, 2011_pace_gossiping, 2012_wolinsky_dissentnumbers, 2013_corrigangibbs_verdict, 2013_leblond_aqua, 2013_wolinsky_hang, 2014_movahedi_secure_anonymous_broadcast, 2014_syta_dissentanalysis
- assumes: Closed group membership and identities; Global traffic adversary; No-silence safety assumption
- compares_with: Intersection attack; Long-term intersection attack limitation; RAC; Three-server Riposte
- defends_against: Disruption attacks; Traffic Analysis
- extends: DC-net
- implements: DC-net; GMP-BULK; GMP-SHUFFLE; Round submission by XOR
- improves_on: DC-net round costs
- instance_of: DC-net
- measures: Dissent latency measurement; Dissent participant scale; Dissent tracing over an hour; Privacy and anonymity performance cost; Protocol cost breakdown
- motivates: UC framework future work
- proves: Negligible security advantage
- provides: Accountability property; Accountability through fair resource allocation; Adoption properties; Anonymity Set; Anonymity bound; GMP-BULK; GMP-SHUFFLE; Integrity property; Node accountability; One message per member per round
- requires: All members participate; Closed known-membership group; Gossip liveness wrapper; IND-CCA2; Trust at least one server
- uses: Anytrust architecture; Browser VM isolation; Cryptographic hash; DC-net; Dissent shuffle and bulk phases; GMP-BULK; GMP-SHUFFLE; Go/no-go and blame phases; Key shuffle; PeerReview

## PQXDH  [concept_pqxdh]  (protocol; 27 papers)
Asynchronous key agreement lets Alice send encrypted initial data while Bob is offline, establishing a shared key with mutual public-key authentication. It provides post-quantum forward secrecy and cryptographic deniability, but mutual authentication still relies on discrete-log hardness in this revision.
Papers: 2016_signal_double_ratchet_spec, 2023_collins_real_deniability, 2023_cremers_keeping_up_kems, 2023_kret_pqxdh_blog, 2023_signal_pqxdh_spec, 2024_apple_pq3, 2024_bhargavan_pqxdh, 2024_collins_dr_tight
- assumes: Active quantum protection excluded; EUF-CMA; IND-CCA; Maximum-exposure model; Untrusted key distribution server
- attacks: KEM Re-Encapsulation Attack; KEM re-encapsulation attack; Public Key Confusion Attack; Public key confusion attack
- contradicts: OPK security limitation; Signed prekeys
- defends_against: Harvest Now, Decrypt Later Attack
- extends: Signal Protocol; X3DH
- implements: Combined shared secret
- improves_on: X3DH
- instance_of: Formal model scope
- measures: Attack discovery runtime; Proof runtime; Tens of millions of users
- motivates: Repeat initial PQXDH message
- part_of: Signal Protocol
- proves: Classical computational security theorem; CryptoVerif computational analysis; Non-constructive simulator; Post-quantum computational security theorem; ProVerif symbolic analysis; Symbolic security theorem
- provides: Double Ratchet; Forward Secrecy; HNDL protection; KEM ciphertext; Mutual authentication; Offline deniability; One-time prekey deletion; Quantum authentication limitation; Quantum protection scope; Session independence
- requires: Additional KEM binding property; Cross-protocol KDF confusion; KEM key binding; Kyber-1024 comparison configuration; Public-key infrastructure
- uses: Asynchronous server key service; Authenticated Encryption with Associated Data; Curve DH key schedule; Double Ratchet; Full and reduced handshake modes; HKDF; Initial AEAD ciphertext; Key encapsulation mechanism; Kyber; ML-KEM

## Differential Privacy  [concept_differential_privacy]  (primitive; 43 papers)
The paper relates its information theoretic protection goal to differential privacy but says the paradigms are not directly comparable: differential privacy concerns datasets differing in one individual entry and preventing obviously diverging algorithm outputs.
Papers: 2013_backes_anoa, 2013_boutet_decentralizing, 2014_oya_dummies, 2015_vandenhooff_vuvuzela, 2016_angel_pung_1, 2016_jansen_safely_measuring_tor, 2016_lazar_alpenhorn, 2017_alexopoulos_mcmix
- assumes: Bounded activity adjacency; One honest collector machine
- compares_with: Composed query leakage risk; Information theoretic anonymity guarantee; Pufferfish; Rényi differential privacy; Statistical privacy
- defends_against: Client AS diversity; Client country diversity; PrivEx aggregate analytics; Store-and-forward anonymous delivery
- extends: Adaptive composition across rounds; Personalized Existing Edge Differential Privacy
- instance_of: Alpenhorn; Complete-graph gossip privacy guarantee; Karaoke; Privacy parameter target; Secure stream-processing approaches; Stadium; Vuvuzela
- leaks: Karaoke; Stadium
- measures: Complete-graph privacy failure for Algorithm 1; Inherent source anonymity
- proves: MAP guess bound; MLE guess bound; Observation probability bound
- provides: Adjacent communication actions; DP family tradeoffs; Per-user privacy bound; PrivCount measurements; Privacy across hundreds of loss rounds; Privacy upper bound for cobra and Dandelion
- requires: Anonymous Broadcast Channel; Cover Traffic; Daily action bounds
- uses: Anytrust group; Distributed measurement with private set union; Mix batch size; Privacy notions; Vuvuzela

## Loopix  [concept_loopix]  (protocol; 45 papers)
Loopix has low latency and high throughput, with latency demonstrated below 2 seconds for 500 clients; its fixed route length suggests latency may not rise much with more users. Its asynchronous operation trusts a service-provider node, which learns the number and timing of real messages received; privacy is uneven across hop paths.
Papers: 2017_das_trilemma, 2017_kwon_atom, 2017_piotrowska_loopix, 2017_tyagi_stadium, 2018_lazar_karaoke, 2019_kuhn_privacynotions, 2019_lazar_yodel, 2019_leibowitz_silentmixes
- assumes: Bounded compromised users; Global passive adversary; Privacy-friendly lookup assumption; Semi-trusted relay assumptions
- compares_with: Adversary model; Anonymity Trilemma; Differential Privacy; Latency tradeoff; Link-based dummies; Miranda mix network; Riffle; Stadium comparison parameters; Streams; Tor
- contradicts: Counting-Bound; Recipient anonymity; Robustness
- defends_against: (n−1) attack; Traffic Analysis; Traffic correlation attack
- implements: Loopix prototype
- instance_of: Mix networks; Mixnet
- leaks: Online/offline intersection inference
- measures: Overall message latency; Privacy notions; Relay delay overhead; Relay throughput
- motivates: Continuous mixnet integration challenge
- provides: Anonymity; Latency-bandwidth-cover tradeoff; Message indistinguishability; Metadata Privacy; Mixnet tradeoffs; Receiver unobservability; Sender online unobservability; Third-party sender-receiver unlinkability; Unreliable datagram service
- requires: End-to-end reliability responsibility; Established provider architecture
- uses: Cover Traffic; Cover traffic; End-to-end dummy traffic; Funnel and compute role separation; Independent per-message paths; Layered mix routing; Mix loop cover for active attack detection; Offline message storage; Onion Routing; Poisson Mix

## Kademlia  [concept_kademlia]  (protocol; 44 papers)
Ethereum inherits Kademlia artifacts despite rarely using its logarithmic content discovery property. The chunk contrasts Ethereum’s limited use of node-ID-to-bucket mapping with Kademlia’s public mapping requirement for iterative content lookup.
Papers: 2011_timpanaro_i2p, 2012_chaabane_ontology, 2013_ciancaglini_keybased, 2013_tox_protocol_spec, 2015_kermarrec_want_centralized, 2015_maloney_dpush, 2015_roos_impossibility_self_stabilization, 2015_unger_sok_securemessaging_tr
- assumes: Kademlia eclipse-resistance conditions
- attacks: Eclipse Attack
- compares_with: DHT lookup latency tradeoff; Decentralized uniform peer sampling; Streamr trackers
- extends: Hierarchical DHT identifiers
- implements: Bucket refresh interval; Discovery table; Key lookup routing; Subnet bucket admission limit
- instance_of: Distributed Hash Table; Transport privacy layer
- measures: DHT deadline failure; DHT lookup overhead; Kademlia lookup hops; Kademlia routing memory
- proves: Kademlia lookup bound; Logarithmic routing bound
- provides: Forwarding request origin ambiguity; Kademlia routing table size; Routing origin ambiguity
- requires: Kademlia bucket parameters; Kademlia churn; Node ID manipulation
- uses: Bucket size k; Distributed Hash Table; Double hashing; Kademlia ID and routing parameters; Kademlia XOR distance; Kademlia k-buckets; Kademlia parallelism α; Opportunistic routing table maintenance; Reachable node count; XOR distance buckets

## Random oracle simulation  [concept_random_oracle]  (mechanism; 42 papers)
A random-oracle hash of the keyword supplies a μ-bit fingerprint, concatenated with the value. In the probabilistic key-value map construction, ε=2^(−μ/2) by the Birthday paradox; the chunk also describes checking the fingerprint to detect false positives.
Papers: 2001_bellare_keyprivacy, 2012_libert_anonymousbe, 2015_dziembowski_proofsofspace, 2017_alwen_scrypt, 2018_giacon_kem_combiners, 2018_poettering_asynchronous_rke, 2019_bernstein_sphincsplus, 2020_alwen_mls_insider
- assumes: Full-redundancy AKEM construction; Random-oracle MAC forgery bound
- defends_against: Claw finding; Hash collision
- implements: External oracle input collision abort
- part_of: Quantum random oracle model
- proves: Birthday paradox
- requires: Classical computational security theorem; PQXDH malicious initiator deniability; PQXDH malicious initiator with honest keys; X3DH

## Vuvuzela  [concept_vuvuzela]  (system; 33 papers)
A scalable private point-to-point text messaging system that hides message data and metadata against an adversary observing and tampering with network traffic and controlling all but one server. Its reported prototype reached 68,000 messages/sec for 1 million users at 37-second end-to-end latency.
Papers: 2015_vandenhooff_vuvuzela, 2016_angel_pung_1, 2016_lazar_alpenhorn, 2017_alexopoulos_mcmix, 2017_das_trilemma, 2017_kwon_atom, 2017_piotrowska_annotify, 2017_piotrowska_loopix
- assumes: Availability condition; Cryptographic assumptions; Distributed provider trust model; Global network attacker; Honest user fraction; No side-channel leakage; Strong network adversary
- compares_with: Anonymity Trilemma; Dissent; Per-epoch mailboxes; Private Information Retrieval; Pung long-lived messages; Tor
- contradicts: Dialing forward secrecy loss; Group privacy limitation; Large file limitation; No metadata leakage
- defends_against: Entry server DoS mitigation; Strong global traffic adversary; Traffic Analysis
- implements: Conversation and dialing protocols
- improves_on: Anonymity Set
- instance_of: Mixnet
- leaks: Key Privacy
- measures: Amortized cost per user; Bandwidth comparison; Bandwidth costs; Client throughput; Conversation bandwidth; Conversation latency; Dialing invitation load; Dialing round wait; Prototype throughput and latency; Server monthly cost
- proves: Joint noise privacy; Noise privacy lemma
- provides: Computational differential privacy; Differential Privacy; Forward Secrecy; Metadata protection; Per-user privacy bound; Scalable private messaging result; Scale relative to prior systems; Sender anonymity
- requires: At least one honest server; Dialing PKI; Vuvuzela privacy budget
- uses: All-node paths; Constant-rate padding; Conversation protocol; Cover Traffic; Dead drop; Dialing protocol; Differential Privacy; Fixed exchange count; Minimized observable variables; Mixnet

## Oblivious Message Retrieval  [concept_oblivious_message_retrieval]  (concept; 30 papers)
Lets a recipient detect and retrieve pertinent messages from a bulletin board with privacy against computationally bounded adversaries. The paper's schemes use FHE and homomorphically encoded sparse random linear codes; practical variants report about 9 bits per message for retrieval and about 20 ms to decode 50 messages from 500,000.
Papers: 2016_sun_pircapacity, 2021_javani_aot, 2021_liu_omr, 2021_madathil_privatesignaling, 2022_barman_groove, 2022_fleischhacker_compressencrypted, 2022_penumbra_fmd, 2022_penumbra_fmd_spec
- assumes: OMR adversary model
- attacks: Retrieval overflow
- compares_with: Expected messages downloaded; Fuzzy Message Detection; Private Information Retrieval; Private Signaling; Relationship unobservability
- contradicts: Sender anonymity
- defends_against: Traffic Analysis
- implements: Homomorphic message bucket filtering
- improves_on: Linear payment scanning; PXE tag scan; Recipient retrieval cost
- instance_of: InstantOMR; OMR public board workflow; SophOMD; SophOMR
- measures: False positive and false negative rates; Liu Tromer prior cost; OMR costs; OMR scan cost
- proves: Recipient anonymity
- provides: Digest; End-to-end anonymity; False negative rate εn; False positive rate εp; Key Privacy; OMR recipient privacy; Receiver Privacy; Receiver privacy; Recipient anonymity; Recipient privacy
- requires: Detection key; OMR recipient-chosen bound k̄; Strong detection-key-unlinkability
- uses: Brakerski/Fan-Vercauteren (BFV); Bulletin board model; Clue; Detector; Detector servers; Fully Homomorphic Encryption; Homomorphic encryption; OHE masking; OMR homomorphic decryption; Private Information Retrieval

## Anonymity  [concept_anonymity]  (property; 33 papers)
Defined by computational indistinguishability between scenarios swapping recipients of two honest senders’ messages, when inputs and outputs for adversarial parties agree. The motivating goal hides sender-recipient relationships even from Bob and a global traffic observer.
Papers: 2001_bellare_keyprivacy, 2009_goldberg_mpotr, 2010_pfitzmann_terminology, 2012_elahi_guards, 2013_gelernter_limits_provable_anonymity, 2014_backes_mator, 2015_zhang_tor_quantum_handshake, 2017_kim_sgxtor
- assumes: Attacker perspective
- compares_with: Key Privacy
- extends: Quasar
- instance_of: Indistinguishability-based anonymity framework; Key Privacy
- leaks: FSPD
- measures: Partial identity anonymity set
- motivates: Zcash
- proves: Anonymity concrete bound
- provides: Metadata Privacy
- requires: Anonymity Set; Global-observer packet-volume condition; Hybrid KEM; One-time signature; Trial Decryption
- uses: Perfect zero-knowledge; Statistical hiding commitments; Statistically pseudorandom function

## Waku  [concept_waku]  (protocol; 30 papers)
The Waku Network is an open-access, decentralized peer-to-peer messaging infrastructure for dApps. It offers routing, filtering, selective message delivery, and historical storage and retrieval for nodes ranging from servers to resource-constrained mobile devices.
Papers: 2019_status_secure_transport_spec, 2019_vac_waku1_spec, 2019_vac_waku_mail_spec, 2020_status_waku_usage_spec, 2020_vac_waku2_filter_spec, 2020_vac_waku2_message_spec, 2020_vac_waku2_relay_spec, 2020_vac_waku2_spec
- assumes: Passive adversary model; Passive protocol-following adversary; Static adversarial model
- contradicts: Confidentiality, integrity, and authenticity out of scope; Forward Secrecy
- extends: GossipSub; Whisper
- implements: Decentralized bundle retrieval; Publish/Subscribe; Waku network graph
- improves_on: Whisper
- instance_of: Publish/Subscribe
- leaks: Topic-interest disclosure
- motivates: Unlinkability
- provides: Adaptive nodes; Anonymous subscription unsupported; Authenticity; Bandwidth savings; Bloom filter topic projection; Censorship resistance; Confidentiality; Envelope metadata; Filter; Integrity
- requires: devp2p
- uses: 11/WAKU2-RELAY; 12/WAKU2-FILTER; 13/WAKU2-STORE; 19/WAKU2-LIGHTPUSH; Content-topic filtering; DNS-based discovery; Filter-push protocol; Filter-subscribe protocol; Gossip flooding; GossipSub

## Bitmessage  [concept_bitmessage]  (protocol; 35 papers)
A trustless decentralized peer-to-peer messaging system that provides anonymity by flooding messages across the network and privacy by encrypting them with the receiver’s public key. Sending requires proof-of-work, averaging four minutes; offline receivers force the sender to recompute it, and receivers decrypt every message.
Papers: 2012_bitmessage_protocol_specification, 2012_bitmessage_wiki_changelog, 2012_bitmessage_wiki_faq, 2012_warren_bitmessage_whitepaper, 2013_kazemzadeh_overlay, 2013_leblond_aqua, 2013_mega_social_overlays, 2014_melara_coniks
- assumes: Trustless peer-to-peer operation
- compares_with: Streamr trackers
- hides: Orisi
- implements: PyBitmessage
- improves_on: Broadcast group clustering
- instance_of: Publish/Subscribe; PyBitmessage; Python 3 implementation; Uniform flooding cost
- leaks: Bitmessage global message storage; Public seeding advertisements
- measures: Connection startup delay; Echo response latency
- provides: Attachment size comparison; Authenticated broadcast subscription; Connection limits; File-level peer discovery; Fully distributed definition; Initial download latency; Message expiry; Offline message retention; Passive operating mode; Seeder upstream cost
- requires: Bitmessage 48-hour receipt window; Bitmessage proof of work; Bitmessage recipient trial decryption; Per-message proof of work; Proof of Work
- uses: Best-effort peer forwarding; Bitmessage address; Bitmessage network broadcast; Bitmessage streams; Connection-wide message propagation; ECIES; ECIES payload encryption; Hashed public key address; Hierarchical streams; I2P

## Peer Sampling  [concept_peer_sampling]  (mechanism; 36 papers)
Gossip peer-sampling protocols periodically exchange neighbor-list portions with randomly selected peers to create views that quickly become statistically representative of the global network. The quality of overlays, information dissemination, and distributed consensus depends on these views.
Papers: 2002_douceur_sybil, 2011_dangelo_adaptive, 2011_pace_gossiping, 2011_sanchezmonedero_ddsbloom, 2011_sarela_bloomcasting, 2012_matos_brisa_combining, 2012_rahimian_locality_awareness, 2013_boutet_decentralizing
- assumes: NAT filtering
- attacks: Balanced attack
- compares_with: Membership maintenance
- measures: Four-round gossip dissemination; Partition thresholds by view size; Randomness distortion; Simulation setup; Stale references
- provides: Gossip protocols; Local randomness guarantee; Stake-preferred gossip backbone; Topic-Connected Overlay; Uniform random peer sample; Workflow execution continuity
- requires: Identity distinctness; Protocol round period
- uses: DNS peerlist; Discovery table; Gossip protocols; Peer clustering; Push-pull exchange

## libp2p  [concept_libp2p]  (artifact; 38 papers)
libp2p can provide the required underlay functions and is the designated connectivity driver in the specification. The initial Go implementation instead uses Ethereum devp2p/rlpx over TCP/IP with custom cryptography.
Papers: 2016_facebook_secretconversations, 2019_burgel_hopr, 2019_vyzovitis_gossipsub_v01, 2020_leastauthority_gossipsub_audit, 2020_vac_waku2_message_spec, 2020_vac_waku2_spec, 2021_antunes_pulsarcast, 2021_berty_wesh_protocol
- compares_with: Nostr
- implements: Connection manager; GossipSub; IPFS; Kademlia; Mixnet; Signal Protocol
- part_of: IPFS
- provides: Floodsub; GossipSub; NAT traversal; Peer discovery; PeerID pseudonymity; Publish/Subscribe; libp2p network-layer defenses
- requires: Routing table capacity
- uses: Circuit Relay; GossipSub; Kademlia; Swarm connections

## Rendezvous Point  [concept_rendezvous_point]  (mechanism; 34 papers)
The PSIRP-side forwarding process is delegated to a Rendezvous point, which matches subscriptions to publications and initiates dissemination. The Rendezvous function tracks publication versions so only newly generated publication messages are delivered.
Papers: 2011_giannaki_supporting, 2011_pace_gossiping, 2011_sarela_bloomcasting, 2012_rahimian_locality_awareness, 2012_setty_poldercast, 2013_biryukov_trawling, 2013_chen_reliable, 2013_stais_errorcontrol
- extends: Rendezvous backends; Rendezvous point types
- implements: Hidden-service peer connections; NAT relaying; PSIRP architecture; Sparse-mode rendezvous tree; Topic-Connected Overlay
- instance_of: Distributed Hash Table
- motivates: Deployment and security study; Scribe churn miss ratio
- provides: Forwarding Identifier (FId); Guard discovery; LIPSIN dissemination; Publisher-to-RP bidirectional path; Scope identifier (SId)
- requires: Hidden service descriptors
- uses: Decentralized hole punching; Distributed Hash Table; Onion Routing; Rendezvous Id and Scope Id; Smart Cache (SC)

## Scribe  [concept_scribe]  (protocol; 26 papers)
Scribe creates multicast infrastructure for many groups of varying sizes. Grouping may use randomness or node similarities, but complex subscriptions make grouping difficult and grouping without suitable topic information may not fit the entire pub/sub network.
Papers: 2012_baldoni_dynamic_message, 2012_chaabane_ontology, 2012_matos_brisa_combining, 2012_setty_poldercast, 2013_boutet_decentralizing, 2013_buford_applicationlayer, 2013_matos_scaling_up, 2013_rene_erreichen
- attacks: Rendezvous failure and bottleneck
- compares_with: Dissemination efficiency and fault tolerance; Evaluation workloads; Scribe delay ratio; Topic-Connected Overlay; Tree routing tradeoffs
- defends_against: Message loss
- instance_of: Publish/Subscribe; Single Root Per Topic (SRPT); Topic-Based Pub/Sub
- leaks: Cannot suspend publishing; Gratuitous forwarding; Pure-forwarder tradeoff; Rendezvous node bottleneck; Routing overhead; Scribe relay false positives; Scribe unwanted traffic
- measures: End-to-end latency; Pattern detection baseline; Scribe churn miss ratio; Scribe received-message order result
- motivates: Rendezvous tree relay cost
- provides: Quality of Service; Rendezvous-node scalability and fault-tolerance issues; Scribe degree bound; Scribe exact matching limitation; Scribe failure recovery; Scribe payoff distribution; Scribe scalability and repair; Scribe zero duplicate messages
- requires: M2etis
- uses: Active adaptation; Distributed Hash Table; Kademlia; Leave pruning; Multicast tree per topic; Pastry; Pastry DHT; PeerSim; Rendezvous Point; Rendezvous node

## Random oracle model  [concept_random_oracle_model]  (assumption; 33 papers)
The anonymity proof requires the ROM to keep tagging-key derivations consistent when future corruption or challenge use is not yet known; lazy sampling is used. The text says avoiding ROM would require a binary guess per pre-shared key, causing exponential blow-up.
Papers: 2001_bellare_keyprivacy, 2009_danezis_sphinx, 2016_boneh_balloon, 2016_cohngordon_signal, 2017_bos_kyber, 2018_liu_keyinsulatedstealth, 2018_unger_deniable, 2019_chase_signal_private_groups
- assumes: Encoding versus signature separation; Key-dependent signature plaintext; Non-interactive zero-knowledge proof of knowledge; Poseidon2; SHA-512; Signal Protocol; Tight security reduction
- instance_of: Random oracle hash assumption
- proves: Fresh X3DH key indistinguishability
- provides: Random oracle extractability
- requires: CKA one-way security; Straight-line simulators

## Verdict  [concept_verdict]  (system; 21 papers)
A transparency dictionary using SNARK proofs to let clients verify reads and authorized updates. Evaluated at 2^20 label-value tuples, it achieves 4 updates/sec/CPU-core and 2 inserts/sec/CPU-core with a 651-byte amortized per-epoch proof and about 3 ms verification; a deferred-guarantee variant reaches 18–22 updates/sec/core and 9–11 inserts/sec/core with a 290-byte proof and 161 μs verification.
Papers: 2013_corrigangibbs_verdict, 2014_movahedi_secure_anonymous_broadcast, 2014_syta_dissentanalysis, 2015_unger_sok_securemessaging, 2015_unger_sok_securemessaging_tr, 2016_angel_pung_1, 2016_gelernter_anonpop, 2017_barman_prifi
- assumes: Anytrust assumption; Global metadata privacy tradeoff; Mailbox systems correct-server assumption; Overall composition lacks rigorous proof; Threat scope
- attacks: Equivocation attack
- compares_with: Baseline comparison; Bilinear pairing scheme; Byzantine Fault Tolerance; Dissent scale limit; XOR DC-net computation cost
- defends_against: DC-net jamming attack; Denial of service attack; Traffic Analysis
- extends: Dissent; Dissent in Numbers; Membership concealment
- implements: Client/server architecture; DC-net; Epoch commitments and proofs; Hybrid XOR/verifiable DC-nets; Keypal
- improves_on: Adoption properties; DC-net; DC-net round costs; Naive SNARK cost
- instance_of: DC-net; Group arithmetic computation cost; Lack of rigorous security proofs
- measures: 1,000 users at 10 seconds; 100 users at 1 second; 250 active users trace evaluation; Lookup cost; Proof generation CPU limitation
- provides: Anonymity Set; Append-only property; Commitment size; Deferred guarantees variant; Eventual equivocation detection; Resistance to strong traffic observers
- requires: Anytrust assumption; Byzantine Fault Tolerance; Public-key computation overhead
- uses: Append-only hashchain; Chaum DC-net security analysis; Client-side operation replay; DC-net; Derived dictionary; ElGamal encryption; Indexed Merkle trees; Phalanx; Publicly verifiable secret sharing; SNARK

## BitTorrent  [concept_bitcoin]  (system; 31 papers)
Bitcoin is one of four cryptocurrency rendezvous considered. The implementation encodes challenge data in Pay2ScriptHash transaction outputs; up to 20 bytes are placed there, with coins burned, and a separate output funds the response fee.
Papers: 2012_kazemzadeh_introducing_publiy, 2013_vansaberhagen_cryptonote, 2014_bensasson_zerocash, 2014_biryukov_bitcointor, 2014_biryukov_deanonymisation, 2014_fischer_qualityofserviceaware, 2014_gervais_bloomfilters, 2016_biryukov_equihash
- attacks: Supernode deanonymization
- compares_with: Monero address and payload sizes
- implements: Outgoing peer bucket selection; Timestamp tie-break penalty
- instance_of: Nakamoto consensus
- provides: Bitcoin block interval and reward; Bitcoin blockchain; Bitcoin peer address database; Bitcoin peer connection defaults; Bitcoin reputation-based anti-DoS protection; Block component sizes; Bloom-filter adversary; Per-connection address history; Public transaction history; Unauthenticated unencrypted transport
- uses: Bitcoin proof-of-work condition; Block request timeout; Default Bitcoin peer connections; Diffusion; Diffusion broadcast; ECDSA quantum vulnerability; Elliptic Curve Digital Signature Algorithm; Gossip protocols; Hashcash; Proof of Work

## IND-CCA  [concept_ind_cca]  (property; 27 papers)
The honest-removal analysis relies on encrypted preference lists under an IND-CCA scheme so a computationally bounded adversary cannot choose active candidates as a function of an honest candidate; candidates are sampled independently and uniformly from [m].
Papers: 2012_libert_anonymousbe, 2013_kohlweiss_anonymitypke, 2014_chase_algebraicmacs, 2018_bindel_hybrid_kem_ake, 2020_alwen_mls_insider, 2020_bellare_imessage_signcryption, 2020_schwabe_kemtls, 2021_hashimoto_chained_cmpke
- assumes: DCR assumption; DDH assumption; Quantum random oracle model
- attacks: Matrix
- contradicts: CK weak-PFS claim counterexample
- defends_against: Active decapsulation access
- instance_of: Public-key encryption
- measures: Key Encapsulation Mechanism
- motivates: KEM Re-Encapsulation Attack
- proves: OW-PCA
- requires: Negligible distinguishing advantage; Post-quantum computational security theorem; Strong robustness construction bound
- uses: Explicit authentication bound

## Dandelion  [concept_dandelion]  (protocol; 26 papers)
Earlier protocol that forwards transactions for a geometric number of hops with parameter q on a directed-cycle anonymity graph, then diffuses them. Its guarantees assume honest-but-curious adversaries with limited graph knowledge and one transaction per node.
Papers: 2012_bitmessage_protocol_specification, 2013_johnson_usersgetrouted, 2013_wolinsky_hang, 2015_fanti_hidingrumor, 2017_venkatakrishnan_dandelion, 2018_bip156_dandelion, 2018_fanti_dandelionpp, 2018_naumenko_erlay
- assumes: Honest-but-curious adversary
- attacks: Ethereum-specific timing side-channel; Propagation-graph topology exposure; Traffic Analysis
- compares_with: AetherWeave; Dandelion++; Privacy versus dissemination time
- contradicts: Robustness goal
- extends: Dandelion++; Publish/Subscribe
- implements: Dandelion stem and fluff phases
- improves_on: Routing-only anonymity lower bound
- measures: Anonymous gossip latency cost; Dandelion phase tail
- motivates: Anonymity Set; Graph learning precision comparison
- proves: Privacy upper bound for cobra and Dandelion
- provides: Dandelion near-optimal detection region; Expected precision and recall guarantees
- requires: Concealed line structure; Dandelion transaction marker; Reachable-node coverage
- uses: Diffusion; Diffusion broadcast; Fluff phase; Max divergence bound; Per-inbound-edge routing; Privacy graph; Random outbound destinations; Random walk with probabilistic die out; Restricted forwarding; Route shuffling

## Pseudorandom function  [concept_pseudorandom_function]  (primitive; 28 papers)
The PRF assumption supports rules that treat a keyed hash as indistinguishable from a fresh nonce when the message has not already been hashed and the key is not used elsewhere. Additional rules handle oracle access and hashes whose inputs depend on their own hashes.
Papers: 2010_corrigangibbs_dissent, 2014_bensasson_zerocash, 2016_angel_pung_1, 2016_jakobsen_bootstrap_anonymous, 2018_ando_practical_onion_routing, 2018_giacon_kem_combiners, 2019_brendel_pq_x3dh, 2019_corrigangibbs_sublinear_pir
- assumes: Collision resistance assumption; Decisional Diffie–Hellman assumption
- compares_with: Random oracle model
- implements: Dialing accept; Dialing request; Nonce plus PRF tag; Random oracle model
- proves: Random sample collision bound

## Fuzzy Message Detection  [concept_fuzzy_message_detection]  (primitive; 23 papers)
The paper explores post-quantum fuzzy message detection, also called fuzzy tracking, and proposes two constructions. In its performance setup, one construction targets 104-bit computational and 40-bit statistical security; the scalable construction targets 115-bit security with negligible failure probability.
Papers: 2021_beck_fmd, 2021_hashimoto_pq_x3dh_deniable, 2021_liu_omr, 2021_madathil_privatesignaling, 2021_seres_fmdfalsepositives, 2022_penumbra_fmd, 2022_penumbra_fmd_spec, 2022_penumbra_protocol_detection_memo
- attacks: Traffic Analysis; Wildcard ciphertext attack
- compares_with: Bloom Filter; OMR recipient privacy; Oblivious Message Retrieval; Oblivious message access; Private Signaling (PS); Receiver privacy; Recipient identity privacy
- contradicts: Differential Privacy; Recipient anonymity
- extends: Outsourced detection key
- implements: Flag ciphertext test
- improves_on: Linear payment scanning; Post-quantum fuzzy tracking; Shared-secret assumption
- leaks: False-positive rate visibility
- measures: FMD costs; Post-quantum FMD costs; Scalable fuzzy tracking costs
- proves: Incoming Count DP Bound; Personalized Existing Edge Differential Privacy
- provides: Anonymity Set; Detection ambiguity; FMD correctness; FMD detector; FMD fuzziness; False positive trade-off; False positives as cover traffic; False-positive rate p; Fractional probability construction; Local filtered stream
- requires: Detection ambiguity; FMD correctness; Fuzziness; Key Privacy
- uses: Anonymity Set; Cover Traffic; Cover traffic; Detection keys; False Positive Rate; False-positive detection rate; False-positive rate ρ; Global state-update stream; Post-quantum FMD parameters; Scalable fuzzy tracking parameters

## Pung  [concept_pung]  (system; 25 papers)
Pung supports asynchronous CPIR storage, but its low latency applies when one user submits and others do not; messages are processed sequentially, with quadratic horizontal scalability in user growth. Its asynchrony is partial when used as CUS.
Papers: 2016_angel_pung_1, 2016_lazar_alpenhorn, 2017_alexopoulos_mcmix, 2017_barman_prifi, 2017_tyagi_stadium, 2018_angel_sealpir, 2018_lazar_karaoke, 2018_mp3_privatepresence
- assumes: Endpoint compromise limit; Global adversary model; Pung single-server security setting; Shared-secret assumption
- compares_with: Conversation protocol; Express; Express latency versus Pung; Latency at 32,768 users; Pung dialing incompatibility; Server CPU per subround; Single-server latency result; Social graph privacy; Talek retrieval cost; Vuvuzela privacy budget
- contradicts: No censorship resistance
- extends: Alpenhorn
- hides: Metadata Privacy
- implements: Mailbox label derivation; Oblivious BST retrieval; Round-based requests
- instance_of: DC-net; Private Information Retrieval; Pung bandwidth comparison
- measures: Computational cost reduction; Daily hosting costs; Four-server throughput; Large-message, medium-k regime; Multi-retrieval network cost; Pung data egress cost; Pung performance improvement; Pung retrieval cost; Quadratic scalability; Single retrieval network cost
- provides: Applicable applications; Cold-call limitation; High network cost limitation; Pung group communication support; Relationship Unobservability
- requires: FHE cost comparison; Liveness assumption; Message size privacy; One short-term entry per online user; Participation every round; Participation when idle; Shared secret setup
- uses: Authenticated Encryption; Computational PIR (CPIR); Private Information Retrieval; Probabilistic multi-retrieval; Pseudorandom function; Pung BST retrieval; Pung Bloom filter retrieval; Pung explicit retrieval; Pung multi-retrieval; XPIR ciphertext size

## I2P  [concept_i2p]  (protocol; 25 papers)
A decentralized anonymous peer-to-peer network using multilayer encryption, garlic routing, and two-hop unidirectional tunnels. The chunk reports about 45,000 active routers, over 15,000 daily users and services, and around 4,000 floodfill routers operating daily.
Papers: 2011_timpanaro_i2p, 2013_ciancaglini_keybased, 2015_sun_raptor, 2016_kysek_minode_readme, 2018_davidson_privacypass, 2018_hoang_i2p, 2018_lewis_cwtch, 2018_shirazi_survey_routing_anon
- attacks: Cheap node attack; Eclipse Attack
- compares_with: Eclipse Attack; Global network adversary; Onion Routing; Tor
- implements: Directed router tunnel graph; Unidirectional tunnels
- instance_of: Three-month measurement setup
- leaks: ISP visibility
- measures: Three-month network measurement
- provides: Bundled garlic messages; Destination-router decoupling; Gateway visibility; Measurement privacy scope; Public ID and IP unlinkability
- requires: Router bandwidth contribution; SAMv3 bridge
- uses: Authenticated key agreement work; DLM requests for RouterInfos; Distributed Hash Table; Floodfill RouterInfo propagation; Garlic Routing; Garlic encryption; Garlic routing; Garlic routing and tunnels; I2P bid scheduling; I2P dynamic selection weights

## Key Privacy  [concept_key_privacy]  (property; 27 papers)
A weak anonymity property: an adversary with public keys and a decryption oracle cannot tell which key encrypted a ciphertext; the chunk notes FMD detection ambiguity does not generally imply it, but Theorem 5 gives a modified implication when p=1.
Papers: 2001_bellare_keyprivacy, 2012_libert_anonymousbe, 2014_roos_measuring_freenet, 2016_hopwood_zcash_protocol_spec, 2017_kwon_atom, 2020_alonso_zerotomonero, 2021_beck_fmd, 2021_madathil_privatesignaling
- compares_with: Wrong-key decryption
- defends_against: Server assignment leakage
- hides: Encrypted output note
- instance_of: ANO-CCA; Anonymity; Ciphertext receiver hiding
- provides: Result unlinkability
- uses: Broadcast Encryption

## Denial of service attack  [concept_denial_of_service_attack]  (attack; 26 papers)
The paper distinguishes general network-level DoS, especially attacks on availability-critical servers, from internal anonymous disruption. It does not address general DoS, citing provisioning, selective traffic blocking, and proof-of-life or proof-of-work challenges as known defenses.
Papers: 2002_back_hashcash, 2009_danezis_sphinx, 2010_corrigangibbs_dissent, 2013_corrigangibbs_verdict, 2015_heimgaertner_security, 2017_barman_prifi, 2018_gundogan_hopp, 2018_recabarren_tithonus
- attacks: NDN; Persistent execution buffer; Verdict
- defends_against: Proof of Work; Rate limiting
- instance_of: Wildcard clue spam
- motivates: Centralized broker single point failure; Stateless per-message routing; Traffic Analysis
- provides: DDoS-induced node failure

## Gossip protocols  [concept_gossip]  (protocol; 25 papers)
Gossip disseminates content through random peer exchanges: each user chooses a given number of peers to send fragments to, which are forwarded onward. After some hops, all audience members receive all fragments with high probability; the approach tolerates node arrivals and departures.
Papers: 2011_mega_dissemination_decentralized, 2011_pace_gossiping, 2013_ciancaglini_keybased, 2013_kim_gossip_causal, 2014_dominguez_contribution, 2014_pellegrino_pushingdynamic, 2015_decouchant_collusions, 2015_kermarrec_want_centralized
- attacks: Eclipse Attack
- compares_with: History-bound encryption
- defends_against: Equivocation attack
- extends: (1+ρ)-cobra walk
- implements: Gossip recommendation systems; Local view; Periodic view exchange; Two-view gossip KNN
- improves_on: Backup set; Publication delay under link failures
- leaks: Event consistency tradeoff; Gossip spam dissemination
- measures: Gossip convergence latency
- provides: Accurate P2P KNN; Decoupled resilient communication; Gossip at 20% link loss; Probabilistic dissemination guarantee; RPS overlay diameter; Unknown topology tradeoff; Wireless failure resilience
- requires: Communication graph; Peer Sampling
- uses: Cyclon; Updates and fragments

## Anonymous Credentials  [concept_anonymous_credentials]  (concept; 19 papers)
Credential holders selectively disclose attributes and can prove zero-knowledge statements about them. Unlinkability prevents issuer-verifier collusions from linking issue and show transcripts, assuming an anonymity set and an anonymous communication channel to hide IP addresses.
Papers: 2016_cohngordon_signal, 2021_cwtch_risk_model, 2021_diaz_nym, 2021_kogan_checklist, 2021_martiny_sealed_sender, 2022_jeudy_lattice_anoncreds, 2022_shirali_dcnetsurvey, 2023_agrawal_traceablemixnets
- assumes: Attributes revealed during issuance
- compares_with: TraceIn query
- extends: Attribute-based extension
- hides: Zero-Knowledge Proof
- instance_of: Everlasting Anonymous Rate-Limited Tokens (EARLT); User
- measures: Cryptographic cost estimate; Parameter set 1 sizes; Parameter set 2 sizes; Parameter set 3 sizes
- part_of: Credential system roles; Nym
- proves: Issuance and showing correctness; Unforgeability reduction
- provides: Anonymity among matching users; Credential Unlinkability; Credential anonymity; Credential unforgeability; Credential unlinkability; Issuer-verifier collusion resistance; Minimal disclosure claim; Negligible anonymity advantage; Privacy Pass; Repeated-showing unlinkability
- requires: Additional credentials hardness requirement; Honest organization keys assumed; Non-interactive zero-knowledge proof of knowledge
- uses: Blind Signature; Certificate authority; Commit-Transferrable Signature (CTS); Credential issuance; Credential presentation; Module signature parameter set; Verifier; Zero-Knowledge Proof

## Nym  [concept_nym]  (system; 18 papers)
A network based on Loopix that the paper says does not provide recipient anonymity for asynchronous client messages. Its design periodically constructs a stratified network from mixes and samples them weighted by stake; the study abstracts stake sampling as bandwidth sampling.
Papers: 2021_diaz_nym, 2022_benguirat_mixnetoptimization, 2022_ma_stopping, 2022_shirali_dcnetsurvey, 2023_kocaogullar_pudding, 2023_ma_verasel, 2024_benguirat_betamixing, 2024_diaz_reliability
- compares_with: A posteriori reliability estimation; Cascade continuous mixnet CCM; Mixnet operator delay recommendation
- contradicts: Recipient anonymity
- defends_against: Global Network Adversary; Ingress/egress flow matching
- extends: Loopix
- implements: Acknowledgment routing; Decentralized overlay network; Fixed gateway mailboxes; Fixed-rate client sending; Gateway and mix path resampling; Mixnet; Nym packet route
- instance_of: Adversarial capacity cost; Integrated system model; Mixnet
- provides: Anonymity Set; Baseline observation rate; Capacity-based routing; Five-layer Nym topology; Horizontal scaling; Metadata Privacy; NymVPN
- requires: Bandwidth credentials; Future empirical analysis; Node Stake
- uses: 250,000 NYM stake saturation proposal; Anonymous Credentials; Cover Traffic; Cover traffic and retrieval rate limiting; Delegated stake; Incentivized Node Market; Independent real and cover traffic schedule; Layered topology; Loop cover traffic; Loopix

## Attribute-Based Encryption  [concept_attribute_based_encryption]  (primitive; 23 papers)
CP-ABE encrypts publication contents under access policies; each health professional has a secret ABE key tied to attributes and uses it to decrypt authorized messages. Publication performance includes encrypting an AES-256 key with ABE, then encrypting the data with AES-256.
Papers: 2014_onica_efficient, 2014_picazosanchez_secure, 2015_unger_sok_securemessaging_tr, 2016_onica_confidentialitypreserving, 2017_conan_multiscaledistributed, 2018_arnautov_pubsubsgx, 2018_coroller_position, 2018_saadeh_ppustman
- assumes: CRP trust assumption
- contradicts: Content-filter expressiveness obstacle
- defends_against: Scope limitation is not privacy
- extends: Encrypted matching
- hides: Broker
- improves_on: MQTT
- proves: ABE collusion security
- provides: ABE subscriber group access control; Collusion resistance; Payload confidentiality; Policy-gated payload decryption; Transfer identifier distribution
- requires: Central authority trust

## Karaoke  [concept_karaoke]  (system; 16 papers)
Karaoke supports low-latency, high-throughput messaging with horizontal scalability, but not asynchrony. Its manytrust uses isolated anytrust input and output chains, so a compromised adversarial input/output chain pair leaks metadata for all communications using them.
Papers: 2018_lazar_karaoke, 2019_lazar_yodel, 2020_abraham_blinder, 2020_cheng_talek, 2020_kwon_xrd, 2020_lazar_thesis, 2021_das_divide_and_funnel, 2021_eskandarian_express
- assumes: Computational security assumption; Karaoke honest-server fraction; Malicious-server model; Network-control adversary; Privacy after endpoint compromise; Two honest servers per path
- compares_with: Alpenhorn; Atom; Bloom-filter versus verifiable-shuffle cost; Cost without optimistic indistinguishability; DC-net; Dissent; Latency comparison; Loopix; Private Information Retrieval; Pung
- contradicts: Robustness
- defends_against: Traffic Analysis
- extends: Vuvuzela
- implements: Communication stack
- improves_on: Latency improvement over prior systems
- measures: Experimental setup; Honest-server fraction tradeoff; Implementation and CPU cost; Latency at sixteen million users; Network-loss measurement; Noise per server; Prototype latency at two million users; Server scaling
- provides: All-to-all verification scaling; Differential Privacy; Fixed message size; Karaoke optimistic indistinguishability; No availability guarantee; Optimistic indistinguishability; Traffic visibility
- requires: Out-of-band dialing; Two messages per round
- uses: Bloom Filter; Dead drops; Differential Privacy; Double-access noise; Duplicate removal; Efficient noise verification; Full-mesh topology; Link-balancing noise; Message loss detection; Message swaps

## Zcash  [concept_zcash]  (system; 19 papers)
The analysis finds that most users do not use Zcash’s shielded pool, and identifiable behavior by pool participants significantly shrinks the anonymity set. The authors suggest requiring transactions to use the pool or expanding its use.
Papers: 2016_hopwood_zcash_protocol_spec, 2017_fanti_anonymitybitcoin, 2018_grigg_zip307_light_client, 2018_kappos_zcash_anonymity, 2018_wust_zlite, 2018_zcash_zip307, 2018_zip302_memo_format, 2020_abraham_blinder
- compares_with: Stealth Address
- instance_of: Anonymous cryptocurrencies; UTXO Model
- measures: Zcash shielded output prevalence
- provides: Issued supply cap; Key Privacy; Nonnegative pool balance rule; Shielded pool; Shielded pools; Transaction consensus rules; Transaction value conservation; Transparent pool; Transparent transactions; Zcash challenge capacity
- requires: Block size limit; Consensus dependency; Funding stream consensus outputs
- uses: BIP-37; Block work; CRH-based Merkle tree; Coin serial number; Difficulty target filter; DigiShield-based per-block adjustment; Equihash; Equihash validity and encoding; Full viewing keys; Incoming viewing keys

## zk-SNARK  [concept_zk_snark]  (primitive; 20 papers)
For the Pinocchio protocol, CRS and proof computation require group exponentiations, verification requires one pairing, and a SHA-1 preimage proof takes 12 s CRS generation, 15.7 s proof computation, about 10 ms verification, and 8 group elements (288 bytes).
Papers: 2014_bensasson_zerocash, 2016_hopwood_zcash_protocol_spec, 2021_duguey_thesis, 2021_liu_omr, 2022_taheri_spam_protected_gossip, 2022_taheri_waku_rln_relay, 2022_vac_rln_v1_spec, 2022_xie_zkbridge
- assumes: Groth16 quantum soundness vulnerability; Knowledge-of-exponent assumptions
- hides: Payment anonymity
- implements: POUR zk-SNARK statement
- measures: server verification time; zk-SNARK proving cost; zk-SNARK setup cost; zk-SNARK verification cost
- motivates: Single global ring
- provides: Credentials from legacy signatures; Perfect zero knowledge; Proof of knowledge and soundness; STARK complexity; Snake-eye resistance; Succinct proof size and verification; Transaction detail privacy
- requires: SNARK composition limitation
- uses: Halo 2; POUR circuit size

## Matrix  [concept_matrix]  (system; 17 papers)
The analyzed Matrix implementation has attacks that invalidate end-to-end confidentiality and authentication against a malicious homeserver. The discussion assumes all devices and users performed out-of-band verification for the attacks described; absent that, impersonation is trivial.
Papers: 2015_matrix_federation_api, 2016_ncc_olm_review, 2019_burgel_hopr, 2019_jacob_matrix_glimpse, 2020_jacob_matrix_event_graph, 2020_weidner_decentralized_sgm, 2022_blazy_pcs_taxonomy, 2023_albrecht_matrix
- assumes: Attack scope; Global ordering assumption
- compares_with: DCGKA; Fourteen theoretical attacks
- contradicts: Authentication and confidentiality failure
- implements: Publish/Subscribe; Topic-Based Pub/Sub
- instance_of: Encrypt then Sign; Federated Communication; Sender Keys; Symmetric signcryption
- provides: Duplicate invite delivery; Invite blocking; Join auth chain and state exchange; Knock room state response; No device revocation; Pair-scoped transactions; Reduced join response; Topic-Based Pub/Sub; Unencrypted forged sender
- requires: Authentication requirement; HTTPS JSON baseline; Restricted room join authorization; Room version negotiation; TLS certificate validation; Transaction size limits; make_join template validation; make_knock template validation; send_join validation; send_knock validation
- uses: Cross-signing; Federated homeserver network; Homeserver proxy; Key Request Protocol; Knock-to-invite linking; Matrix Event Graph (MEG); Matrix TLS links; Matrix long-term identity keys; Megolm; Megolm ciphertext authentication

## Stadium  [concept_stadium]  (system; 17 papers)
A distributed metadata-private, point-to-point messaging system that spreads computation across providers and scales by adding servers. Its conclusion says it supports 4× more users than previous systems with servers costing an order of magnitude less to operate.
Papers: 2017_kwon_atom, 2017_tyagi_stadium, 2018_lazar_karaoke, 2019_ando_complexity, 2020_abraham_blinder, 2020_cheng_talek, 2020_kwon_xrd, 2021_das_divide_and_funnel
- assumes: At least one honest server per chain; Cryptographic assumptions; Distributed provider trust; Distributed provider trust model; Global network adversary; Stadium honest-server fraction
- compares_with: A posteriori reliability estimation; Comparison with Vuvuzela; Pung; Selected mean delay levels; Single-server latency result; Tor; Vuvuzela
- contradicts: Anonymity; Robustness; Stadium and Atom #1 fragility
- defends_against: Blending (n−1) attack; Strong global traffic adversary; Traffic Analysis
- extends: Riffle
- implements: Round-based communication; Stadium prototype; Two-layer mixing topology
- improves_on: Distributed provider trust model; Horizontal scalability
- instance_of: Differential privacy performance tradeoff; Mixnet
- measures: Latency tradeoff; Noise deployment parameters; Stadium capacity; Stadium evaluation at 100 servers
- proves: Horizontal scalability
- provides: Bandwidth comparison; Differential Privacy; Horizontal deployment; Horizontal scalability; Linear horizontal scaling; Observable metadata variables; Parallel verifiable shuffles; Recipient anonymity
- requires: Honest mixchain member; Same output chain constraint; Shared key and PKI
- uses: Approximate DP deployment failure probability; Collaborative noise generation; Cover Traffic; Differential Privacy; Hybrid encapsulation; Hybrid verifiable shuffling; Mixnet; Noise submission hashes; Parallel verifiable shuffles; Poisson noise mechanism

## Riffle  [concept_riffle]  (system; 20 papers)
A mix network requiring all messages through all mixes, with a logarithmic number of mixes in the comparison. It uses PIR after verifiable shuffling and assumes all clients send each round; Counting-Bound only applies to the one-sender special case.
Papers: 2016_angel_pung_1, 2016_kwon_riffle, 2017_alexopoulos_mcmix, 2017_barman_prifi, 2017_das_trilemma, 2017_piotrowska_loopix, 2017_tyagi_stadium, 2018_mp3_privatepresence
- assumes: Anytrust assumption; Client-server bandwidth priority; Confidentiality scope; Intra-group scope; Mailbox systems correct-server assumption; One honest server assumption; Separate server operators; Unprevented false accusation
- compares_with: 10,000-user upload examples; Anonymity Trilemma; Counting-Bound; Dissent; MCMix; PIR resource costs; Riposte upload size; Social graph privacy; Tor
- defends_against: Intersection attack; Mis-authenticated upload attack; Traffic Analysis
- implements: Sender unlinkable broadcast systems
- improves_on: DC-net
- instance_of: DC-net; Mixnet
- leaks: Same permutation linkability
- measures: Client upload bandwidth; File sharing client bandwidth; File sharing performance; File-sharing bandwidth result; Microblogging latency; Microblogging scale result; Server bandwidth
- provides: Accusation process; Client upload cost; Common-case server cryptography; Correctness; Download disruption resistance; Hybrid shuffle verifiability; Hybrid shuffle zero knowledge; Receiver anonymity; Sender anonymity
- requires: Fixed-length blocks and padding; Group churn cost; One short-term entry per online user; PIR every round; Server bandwidth bottleneck; TLS
- uses: Fixed-round messages; Hybrid Verifiable Shuffle; Mixnet; Onion Encryption; PIR XOR masks; Private Information Retrieval

## Key Transparency  [concept_key_transparency]  (primitive; 24 papers)
An application in which a dictionary maps unique identities to public keys, allowing clients to retrieve keys while checking their legitimacy. Non-membership proofs help prevent a service from showing different entries for the same identity.
Papers: 2017_p4t_abuse_detection, 2020_kwon_xrd, 2021_das_divide_and_funnel, 2021_hu_merkle2, 2022_chen_rotatable_zks, 2022_tzialla_transparencydictionaries, 2022_vac_waku2_x3dh_spec, 2023_barnes_rfc9420
- assumes: Malicious KT server; Server Learns Labels and Values
- attacks: Forked view
- compares_with: Auditable CGKA (Au-CGKA); Merkle²
- defends_against: Authentication Service compromise; Fake accounts and subscriptions; Man-in-the-Middle Attack
- implements: Key transparency detection
- improves_on: Certificate Transparency
- instance_of: Authentication Service (AS)
- provides: End-to-end encrypted communication; Monitor operation; Primary device root of trust; Search operation; Server; Shared tree view; Update operation; Verifiable Key Directory (VKD)
- requires: Append-only property; Consistent commitment broadcast; Privacy via access control
- uses: Commitment gossip; Cryptographically protected append-only log; KT commitments and query proofs; Privacy-preserving set intersection protocols; Public untamperable ledger

## Smart Contract  [concept_smart_contract]  (mechanism; 22 papers)
A program triggered by transactions to validate state and automate application processes. Trinity contracts specify stakeholders and signatures, associated topics, and conditions; validators execute them before consensus and recording.
Papers: 2018_ramachandran_trinity, 2019_bu_hyperpubsub, 2020_albreiki_blockchain_oracles, 2020_savolainen_streamr_network, 2021_pasdar_oracle_design_patterns, 2021_tron_swarm_whitepaper, 2022_dzakie_private_blockchain_mqtt_auth, 2023_eip6538_stealthregistry
- defends_against: Inconsistent Logging flag conditions
- implements: Distributed authentication service; Distributed validation flow; Strongly oblivious read-once map (SOROM)
- leaks: On-chain device metadata exposure
- provides: State change audit log; Transparent immutable transaction history
- requires: Blockchain Oracle
- uses: Streamr trackers

## Dandelion++  [concept_dandelion_pp]  (protocol; 16 papers)
Hop-by-hop transaction routing that forwards to two successors in its privacy subgraph. The chunk reports median entropy of 5 bits with 20% adversarial nodes and describes learning over 90% of a simulated privacy subgraph, rising to about 98.5% accuracy with 100 transactions per node.
Papers: 2018_fanti_dandelionpp, 2021_franzoni_clover, 2021_modinger_statistical, 2021_rohrer_kadcast_ng, 2021_tabatabaee_mwdos, 2023_beres_ethp2psim, 2023_bienstock_asmesh, 2023_sharma_p2panonymity
- attacks: Ethereum-specific timing side-channel; Transaction denial of service with aggregations
- compares_with: BitTorrent; Dandelion phase tail; NTSSL
- contradicts: Robustness goal
- defends_against: Botnet adversary; Graph-construction attack; Graph-learning attack; ISP- or AS-level routing adversary; Probe node; Protocol leakage rather than cryptographic break
- extends: Dandelion
- implements: Bitcoin Core prototype
- measures: Mainnet evaluation
- provides: Graph learning; Timed fluff delay; Transaction source privacy
- requires: Stem path latency tradeoff
- uses: Anonymity graph; Asynchronous epochs; Beam stem aggregation; Dandelion++ approximate four regular graph; Diffusion; Embargo map; Intertwined cable paths; Precision-recall metric; Proxy transaction distribution; Pseudorandom forwarding

## Sealed Sender  [concept_sealed_sender]  (protocol; 17 papers)
The two-way conversation solution uses sealed sender for the initial exchange: the initiator sends to the receiver’s long-term identity and communicates the sender’s ephemeral identity; the receiver then replies to that ephemeral identity with a fresh ephemeral identity. The excerpt ends before stating how later communication works.
Papers: 2018_lund_sealedsender, 2019_campion_multidevice_signal, 2019_tyagi_messagefranking, 2021_beck_fmd, 2021_issa_hecate, 2021_martiny_sealed_sender, 2022_hashimoto_mls_metadata, 2023_bienstock_asmesh
- attacks: Denial of service attack; Statistical analysis attacks
- compares_with: Anonymity Wrapper (AW); Authentication verified; Supplemental receiver anonymity
- contradicts: Correspondent device privacy
- hides: Metadata exposure; Sender identity visibility; Signal Desktop
- improves_on: Signal normal authentication
- instance_of: SMF metadata requirement; Split-KEM
- leaks: Observable recipient metadata; Recipient and timing exposure; Recipient identity routing; Sender recipient link leakage; Signal transcript framing scenario; State metadata exposure; Timing and IP correlation
- measures: AMF signature size; Measured message sizes; Sealed Sender computation times
- provides: Sender anonymity; Sender identity hiding; Sender obfuscation
- requires: Delivery token; Quick response assumption; Recipient remains visible; Sender-specific certificate; Temporary state exposure
- uses: Delivery token; Double Ratchet; ECDH; Immediate delivery receipts; Outer envelope encryption; Sealed Sender access key; Sealed sender message flow; Sender certificate; Signal Protocol; Unauthenticated delivery

## Decision Diffie–Hellman assumption  [concept_ddh]  (assumption; 18 papers)
The DDH assumption is used to replace honest-party tags computed from a shared random group element with independent random group elements. The reduction’s bound is multiplied by the number of honest signatures and random-oracle queries.
Papers: 2012_libert_anonymousbe, 2014_chase_algebraicmacs, 2017_chaum_cmix, 2018_mp3_privatepresence, 2019_chase_signal_private_groups, 2019_tyagi_messagefranking, 2019_wang_improving, 2020_kreuter_anontokens
- assumes: Cramer–Shoup example; Tag-based anonymous hint system
- instance_of: Bilinear group
- proves: Key-parameter consistency
- provides: Discrete log assumption; IND-CCA
- requires: Construction 6 CMBT token scheme
- uses: Judge; QueryKDF abort

## Intersection attack  [concept_intersection_attack]  (attack; 21 papers)
If users churn, online/offline status can be correlated with message output patterns to link messages to the set of users who sent them. The chunk says high churn such as 50% each round can mitigate effectiveness, and buddy sets can also help.
Papers: 2003_goel_herbivore, 2012_wolinsky_dissentnumbers, 2014_roos_measuring_freenet, 2016_galteland_cmixattacks, 2016_hayes_tasp, 2016_lazar_alpenhorn, 2017_barman_prifi, 2017_chaum_cmix
- assumes: Global passive adversary
- attacks: 2PPS; Anonymity Set; Dandelion; Fairness; High churn mitigation; Mix networks; Mixnet; Online-user anonymity set; Probe request privacy risk
- implements: Successor set intersection
- motivates: Avoid linkable transmissions; Buddy system

## CRH-based Merkle tree  [concept_merkle_tree]  (primitive; 20 papers)
Used for binding, space-efficient tag commitments and membership openings. Compared with Bloom filters, it avoids false positives and the described membership-test attack, and scales better at high traffic and low p_lot.
Papers: 2014_bensasson_zerocash, 2016_franck_voipdcnets, 2016_hopwood_zcash_protocol_spec, 2018_ramachandran_trinity, 2020_alonso_zerotomonero, 2021_diaz_nym, 2021_hu_merkle2, 2021_pasdar_oracle_design_patterns
- attacks: Auditor
- compares_with: Aegon; Per-pool nullifier set
- hides: Corda attachment oracle
- implements: Slot key erasure
- improves_on: Bloom Filter; RingXKEM server storage; Server signature storage savings
- measures: Merkle path size; Merkle tree computation cost
- provides: Merkle proof index hiding; Merkle scaling; Public measurement verification; Transaction signature-data pruning
- requires: AKD audit bandwidth; Collision Resistance; Collision-resistant hash function; Type-4-1 advantage bound
- uses: Application contracts

## Key Encapsulation Mechanism  [concept_key_encapsulation_mechanism]  (primitive; 19 papers)
A KEM has randomized key generation and encapsulation, and deterministic decapsulation that returns a session key or reject symbol. A δ-correct KEM has probability at most δ that honest encapsulation and decapsulation produce different keys.
Papers: 2015_zhang_tor_quantum_handshake, 2018_bhargavan_treekem, 2018_durak_linear_ratcheting, 2018_giacon_kem_combiners, 2018_poettering_asynchronous_rke, 2019_brendel_pq_x3dh, 2020_schwabe_kemtls, 2021_brendel_pq_deniable_ake
- assumes: Public-channel exposure
- compares_with: PKIC-KEM
- contradicts: Forward Secrecy
- instance_of: Standard KEM
- measures: No size or performance figures in chunk
- provides: ANON-CCA security; Anonymity; IND-CCA; IND-CPA security; Plaintext-awareness; Semantic security
- requires: Three KEM security conditions
- uses: Plaintext-awareness

## Alpenhorn  [concept_alpenhorn]  (system; 15 papers)
A round-based private discovery system based on Vuvuzela. With one million users, each device downloads a 7.5 MB mailbox; delaying downloads for WiFi can increase lookup latency, and a missed round can lose a request. It fails if any single server crashes, goes offline, or deviates from the protocol.
Papers: 2016_angel_pung_1, 2016_lazar_alpenhorn, 2017_kwon_atom, 2018_lazar_karaoke, 2019_lazar_yodel, 2020_kwon_xrd, 2021_ahmad_addra, 2021_beck_fmd
- assumes: Adversary model; Secure client deletion assumption
- attacks: Groove
- compares_with: Binary-tree key size tradeoff; FMD needs no trusted server; Private Information Retrieval; Tor
- defends_against: Man-in-the-Middle Attack; Metadata Privacy; Traffic Analysis
- extends: Vuvuzela
- improves_on: Anytrust versus PIR; Vuvuzela bandwidth comparison
- leaks: Address-book exposure; Groove; Metadata exposed by ordinary services
- measures: Experimental setup; Three-server scale result
- motivates: Fixed preexisting groups
- provides: 10 million-user scale; Ciphertext Anonymity; Client compromise recovery; Differential Privacy; Forward Secrecy; Keywheel; Linear server cost; Lost client-state recovery; Metadata Privacy; Metadata privacy and forward secrecy
- requires: Email reconnection interval; Mixnet; Single-server failure dependence
- uses: Alpenhorn bucket retrieval; Anytrust-IBE; BN-256 security estimate; Bloom Filter; Boneh–Franklin IBE; Constant-rate cover traffic; Cover Traffic; Differential Privacy; Diffie-Hellman; Distributed IBE

## Ed25519  [concept_ed25519]  (primitive; 18 papers)
Session generates Ed25519 keys from a random 128-bit seed rather than a 256-bit seed. SHA-2/512 processing is said to remove bit correlation; 128-bit brute force is considered impractical, and the choice supports 13-word rather than 25-word recovery phrases.
Papers: 2013_tor_prop224_rendng, 2016_hopwood_zcash_protocol_spec, 2016_luo_mpenc, 2016_matrix_megolm_spec, 2016_ncc_olm_review, 2020_alonso_zerotomonero, 2020_autocrypt_spec_1_1, 2021_abegg_supra
- defends_against: Route-list tampering
- implements: Authenticated application messages; BoxMessage; Ed25519 consensus validation rules; Ed25519 point order check
- instance_of: Cyclic subgroups and cofactor; Elliptic curve cryptography
- measures: Signature performance
- part_of: OpenPGP certificate
- provides: Ed25519 rigidity and patent status
- uses: Ed25519 recovery phrase tradeoff; Source route field

## X25519  [concept_x25519]  (primitive; 22 papers)
A traditional key exchange used with ML-KEM in deployed hybrid key establishment and as the second ingredient in the example hybrid KEM. Its ciphertext is retained as an input when the post-quantum first KEM is C2PRI.
Papers: 2013_tor_prop224_rendng, 2016_luo_mpenc, 2016_signal_x3dh_spec, 2018_tor_proposal_269_hybrid_handshake, 2021_alwen_server_aided_cgka, 2023_paterson_threema, 2024_barbosa_xwing, 2024_bhargavan_pqxdh
- contradicts: Public key uniformity
- instance_of: DHKEM-Ell2
- measures: X25519 key reuse
- provides: Nominal group distribution distance
- requires: Both components need weak anonymity
- uses: Omit C2PRI ciphertext from derivation

## IPFS  [concept_ipfs]  (system; 20 papers)
A distributed peer-to-peer version-controlled file system described as having no single point of failure. It uses a global Merkle DAG, content-addressed blocks driven by DHTs, block exchange, and a self-certifying namespace; stored content is accessed via CIDs.
Papers: 2020_albreiki_blockchain_oracles, 2021_antunes_pulsarcast, 2021_berty_wesh_protocol, 2021_guidi_libp2p_bitcoin, 2021_mazmudar_you, 2021_modinger_statistical, 2021_pasdar_oracle_design_patterns, 2021_tron_book_of_swarm
- assumes: Eclipse Attack; Sybil Attack
- compares_with: BitSwap
- implements: Content-addressed storage; Hybrid content storage; Peer and content identifiers
- improves_on: File-level peer discovery
- leaks: PeerID and IP exposure
- provides: CID-based integrity
- uses: Distributed Hash Table; IPFS chunk-topic publishing; Private Information Retrieval; Public-key peer identity; libp2p

## Riposte  [concept_riposte]  (system; 15 papers)
A sender-anonymous bulletin-board system that publishes messages received during each epoch. It uses random write locations, risking collisions; the paper states a 5% collision rate at board size 2.7n with two-message recovery, while the basic sizing is 19.5 times expected messages.
Papers: 2015_corrigangibbs_riposte, 2015_decouchant_collusions, 2016_gelernter_anonpop, 2017_kwon_atom, 2018_mp3_privatepresence, 2020_abraham_blinder, 2021_2pps_pubsubprivacy, 2021_eskandarian_express
- assumes: Riposte coalition threshold
- compares_with: 2PPS; Express; PIB identity-based bulletin board; RemiseBB
- defends_against: Traffic Analysis
- extends: DC-net
- improves_on: Riposte bandwidth efficiency
- instance_of: Compression costs; DC-net
- measures: Large anonymity set result; Large table throughput; Quadratic scalability; Small table throughput
- motivates: RemiseBB
- proves: RIPOSTE popularity threshold
- provides: Anonymous broadcast messaging; Disruption resistance; Forward security; Posterior like probability; Riposte DPF request cost; Riposte epoch anonymity set; Three-server variant; s-server variant
- requires: Riposte WAN communication; Rogue server and clients threat model
- uses: DC-net; Distributed Point Function; Distributed point functions (DPFs); Private Information Retrieval; RIPOSTE parameters; Riposte audit cost

## TLS  [concept_tls]  (protocol; 20 papers)
With one-way authentication, TLS transcripts are argued to be universally deniable because any party can establish a session key with the platform server and forge a transcript; the server still learns sender IP at send time.
Papers: 2015_unger_sok_securemessaging_tr, 2016_kwon_riffle, 2017_barman_prifi, 2019_banno_interworking_layer, 2019_paquin_pq_tls_benchmark, 2019_tyagi_messagefranking, 2020_dias_mqttmecanismo, 2020_schwabe_kemtls
- contradicts: End-to-end encryption limitation
- defends_against: Broker can read unencrypted payload; Global Network Adversary
- instance_of: Authenticated encrypted links and uncompromised crypto
- motivates: TLS for all clients burden
- provides: Client security goals; Deniability; TLS handshake completion time; TLS page retrieval time

## Fully homomorphic encryption (FHE)  [concept_fully_homomorphic_encryption]  (primitive; 17 papers)
FHE lets a detector evaluate circuits over ciphertexts without learning their data or output. OMRt1 works with any FHE scheme satisfying the required wrong-key decryption property; generic construction is asymptotically compact but impractical due to computation and clue size.
Papers: 2017_chen_psihe, 2019_corrigangibbs_sublinear_pir, 2020_das_comprehensivetrilemma, 2021_liu_omr, 2021_tian_iot_pubsub_access_control, 2022_corrigangibbs_pirsublinearamortized, 2022_lazzaretti_nearoptimalpir, 2022_lin_deprir
- assumes: Ring learning with errors; Wrong-key decryption near-uniformity
- hides: ZK-DPPS
- implements: Encrypted parity hints
- improves_on: User coordination assumptions
- motivates: Deep FHE circuit bottleneck; OMR1 multi-user message DoS attack
- provides: Access-pattern privacy; IND-CCA security; IND-CPA security
- requires: Circular security; Collaborative partial decryption; IK-IND-CPA security; IND-CPA security; Security for Q queries; Strong correctness

## Pedersen commitment  [concept_pedersen_commitment]  (primitive; 18 papers)
The commitment uses five independent generators in a prime-order group; it is perfectly hiding and computationally binding if the discrete logarithm problem is hard, with q large enough to encode accounts, nonces and amounts.
Papers: 2014_chase_algebraicmacs, 2015_corrigangibbs_riposte, 2016_hopwood_zcash_protocol_spec, 2018_liu_keyinsulatedstealth, 2019_chase_signal_private_groups, 2019_sonnino_coconut, 2020_alonso_zerotomonero, 2020_yu_stealthschemes
- assumes: Discrete logarithm assumption; Random oracle model
- implements: Output amount commitment
- proves: HID-OR
- provides: Computational binding; Perfect hiding; Zero-Knowledge Proof
- requires: Discrete logarithm assumption

## Blinder  [concept_blinder]  (system; 7 papers)
A Riposte-derived system requiring at least five servers with an honest majority; it assumes all users broadcast and can use a server-side GPU. The chunk reports Spectrum 2× slower than Blinder CPU and 13–17× slower than GPU in unfavorable settings, but 500–7,500×/250–520× faster in favorable settings.
Papers: 2020_abraham_blinder, 2021_2pps_pubsubprivacy, 2022_newman_spectrum, 2023_sasy_sokmetadata, 2024_rosenberg_zipnet, 2026_li_pepper, 2026_tang_dumbomix
- assumes: Finite field parameters; Global active adversary; Stand-alone epoch scope; Synchronous network
- compares_with: CPU scale versus Riposte; GPU speedup over Riposte; GPU speedup versus Riposte; ZIPNet Blinder server speedup
- contradicts: Anytrust Model
- defends_against: Traffic Analysis; Write database collisions
- extends: Distributed Point Function; Riposte
- implements: Anonymous committed broadcast; GPU task migration
- improves_on: Riposte
- instance_of: Compression costs; SUBS
- measures: AWS instance costs; Blinder server aided communication; CPU latency at one hundred thousand clients; CPU latency at ten thousand clients; Client count evaluation; GPU cost per client; GPU decompression share; GPU latency at one million clients; Latency sensitivity to bandwidth; Network settings
- motivates: Asynchronous extension; Differential Privacy; Monero; Zcash
- part_of: Processing phase
- proves: Optimal effective anonymity set
- provides: Anonymity Set; Censorship resistance; Circuit multiplicative depth; DPF query size; Information-theoretic security; Large message support; Malicious adversary resilience; Message chunking tradeoff; Robustness; Robustness overhead
- requires: Broadcast Encryption
- uses: ACB table parameters; AWS cost formula; Authenticated Encryption; Finite-field computation; RPIR; Riposte; Robustness parameter; SMC family; Secure Multi-Party Computation; Shamir secret sharing

## Megolm  [concept_megolm]  (protocol; 8 papers)
Matrix's Megolm permits deriving current ratchet state from any earlier state, allowing an existing device to share an early state so a new device can decrypt later messages. This provides only partial forward secrecy; discarding earlier key material can restore secrecy for corresponding messages.
Papers: 2016_matrix_megolm_spec, 2016_ncc_olm_review, 2021_dimeo_sok_multidevice, 2023_albrecht_matrix, 2023_matrix_core_formal, 2024_cremers_pcs_impossibility, 2024_matrix_symbolic, 2025_msc4268_encrypted_history_sharing
- assumes: Abstract message terms; Finite group peers; No ratchet reseeding; Perfect message ordering
- attacks: Group message replay; Megolm unknown key-share attack
- compares_with: Double Ratchet; Olm; Sender Keys; Signal Protocol
- contradicts: Forward Secrecy; Lack of backward secrecy
- implements: Megolm sender session
- leaks: Lack of transcript consistency; Megolm future key exposure; Megolm initial key history exposure; Transcript inconsistency
- proves: Megolm confidentiality and authentication; Megolm forward secrecy
- provides: Arbitrary forward advancement; Deniability; Matrix partial forward secrecy; Partial forward secrecy; Post-Compromise Security; Repeatable decryption
- requires: Megolm session sharing channel; Post-Compromise Security; Secure channel assumption
- uses: AES-CBC; Curve25519 identity keys; Ed25519 identity keys; HMAC; Megolm Ratchet; Megolm ratchet; Megolm ratchet reseeding schedule; Megolm session and ciphertext signatures; Message authentication and signature; Old ratchet copies

## Proof of Stake  [concept_proof_of_stake]  (protocol; 20 papers)
Razor uses proof-of-stake consensus with Honey Badger BFT; a large number of individual stakers can participate, and majority-staker consensus is used to report values. Stake-based mechanisms can mitigate Sybil attacks, but may face the verifier’s dilemma.
Papers: 2018_ramachandran_trinity, 2018_sattath_quantum_bitcoin_mining, 2020_alangot_eclipsedetection, 2020_albreiki_blockchain_oracles, 2020_cortes_eth2_p2p, 2021_auvolat_basalt, 2021_diaz_nym, 2021_pasdar_oracle_design_patterns
- assumes: Attacker cannot exceed honest work; Honest majority of stake
- attacks: Quantum adversary
- compares_with: Epidemic BFT sampling motivation
- defends_against: Quantum mining stale-rate finding; Sybil Attack
- instance_of: Consensus Protocol
- requires: Low latency goal

## Floodsub  [concept_floodsub]  (protocol; 18 papers)
The first and simplest IPFS/Libp2p PubSub experiment, routing messages by network flooding without forming a CastTree and using external DHTs for peer discovery. It has low latency on small networks but high overhead and bandwidth consumption that limit scaling.
Papers: 2013_mega_social_overlays, 2017_shirazi_multiparty, 2019_vyzovitis_gossipsub_v01, 2020_leastauthority_gossipsub_audit, 2020_savolainen_streamr_network, 2020_vyzovitis_gossipsub, 2021_antunes_pulsarcast, 2021_guidi_libp2p_bitcoin
- attacks: Peer churn during propagation
- compares_with: Broadcastsub specification; Floodsub churn comparison; GossipSub; Sparse mesh advantage
- instance_of: Floodnet refinement of Broadcastnet; Publish/Subscribe
- measures: Bitcoin flooding bandwidth; Flooding bandwidth factor; Floodsub churn delivery; Neighbour publishing DCA; Neighbour subscribing DCA
- motivates: Flood amplification
- part_of: libp2p
- provides: Duplicate delivery tradeoff; Floodsub latency
- requires: Graceful leave guard; New message precondition; No self in neighbor subscriptions
- uses: Distributed Hash Table; Full-message forwarding; Neighbor subscription map; Pending and seen message sets; Per-topic random regular graph; Well-Founded Simulation

## X-Wing  [concept_x_wing]  (primitive; 10 papers)
A general purpose post-quantum/traditional hybrid KEM built from X25519 and ML-KEM-768, intended for most applications including HPKE. The draft targets 128-bit security (NIST PQC level 1) and says it is not interactive key agreement or authenticated KEM.
Papers: 2023_kret_pqxdh_blog, 2024_barbosa_xwing, 2024_rial_outfox, 2025_alagic_best_of_both_kems, 2025_alagic_nistsp800227, 2025_draft_xwing_kem, 2025_gunther_hybrid_obfuscated_kex, 2026_bao_anonymity_xwing
- assumes: Hybrid security condition; ML-KEM IND-CCA assumption; Random oracle model; Random oracle modeling condition; SHA3 PRF assumption; SHA3 random oracle assumption; Strong Diffie-Hellman assumption
- compares_with: Generic combiner comparison; ML-KEM binding comparison
- implements: Ciphertext rejection fallback; Direct X25519 DH; HPKE KEM interface; Omit ciphertext from hash; Parallel KEM combiner; TLS 1.3 key exchange use
- instance_of: Hybrid KEM; Parallel-style KEM combiner; Quantum Superiority Fighter
- measures: Decapsulation cycles; Encapsulation cycles; Key generation cycles; X-Wing performance gains
- proves: Reduction query cost
- provides: 128 bit target security; 128-bit security target; Fixed key and ciphertext sizes; Hybrid robustness claim; Hybrid shared secret sizes; IETF standardization effort; IND-CCA security; Implementation checks; Key Privacy; Unauthenticated KEM
- requires: Ciphertext Second Preimage Resistance; FIPS-driven component ordering; Fujisaki–Okamoto specificity; ML-KEM encapsulation key check
- uses: Decapsulation key expansion; Expanded decapsulation key cache; ML-KEM; Multi-target protection token; Randomized encapsulation; SHA3-256; SHAKE256; X-Wing combiner; X25519

## Stealth Address  [concept_stealth_address]  (mechanism; 14 papers)
The sender efficiently generates a one-time address from the receiver’s public key; the receiver can identify it using the private key. In Bitmessage Plus it protects the communication relationship and lets receivers filter transactions without decrypting each message.
Papers: 2018_liu_keyinsulatedstealth, 2020_alonso_zerotomonero, 2020_minaei_moneymorph, 2020_yu_stealthschemes, 2021_shi_bitmessage_plus, 2022_yin_hdwalletstealth, 2023_eip6538_stealthregistry, 2023_kovacs_umbra_anonymity
- assumes: Repeated payer randomness exception
- attacks: Key-exposure attack
- compares_with: Silent Payments
- defends_against: Cold-address material leakage
- extends: Identity-Based Encryption (IBE)
- hides: Stealth meta-address
- implements: Stealth address derivation equations; VerifyKeyDerive
- instance_of: ERC-5564
- provides: Ethereum; Key Privacy; Prospective user anonymity; RLN-V1 membership set; Recipient privacy goal; Single-use stealth address; Traditional stealth address linkability; Transaction unlinkability
- uses: Ephemeral public key registry; Stealth meta-address; Tracking server

## Hybrid KEM  [concept_hybrid_kem]  (protocol; 17 papers)
In the OQS-OpenSSL 1.1.1 instantiation, each negotiated group combines two algorithms, concatenates their public keys and ciphertexts, and concatenates the shared secrets for the TLS 1.3 key schedule. The paper motivates hybrid use by early adopters seeking post-quantum long-term forward secrecy while retaining ECDH.
Papers: 2018_bindel_hybrid_kem_ake, 2019_paquin_pq_tls_benchmark, 2020_bellare_imessage_signcryption, 2021_brzuska_mls_draft11, 2024_apple_pq3, 2024_fiedler_pqxdh_analysis, 2024_fiedler_pqxdh_deniability, 2024_nist_fips203
- assumes: Active security requirement unresolved
- motivates: Commit communication cost metric; Memory-sensitive lattice problem
- provides: At least one component remains secure; At-least-one-component security condition; Hybrid assumption and implementation hedge; Key Privacy; Supported-group recommendation status
- requires: Hybrid session initialization; IND-CCA KEM choice; Values requiring secrecy
- uses: ECDH; Robust KEM combiner

## HKDF  [concept_hkdf]  (primitive; 16 papers)
HMAC-based key derivation function used by TLS 1.3 with the concatenated shared secrets. NIST guidance approves two distinct shared secrets when the first is computed by a FIPS-approved key-establishment scheme.
Papers: 2016_matrix_megolm_spec, 2016_matrix_olm_spec, 2016_signal_double_ratchet_spec, 2019_burgel_hopr, 2020_schwabe_kemtls, 2021_duguey_thesis, 2022_barnes_rfc9180, 2022_vac_waku2_x3dh_spec
- assumes: Pseudorandom function; Random oracle model
- implements: Forward Secrecy
- instance_of: Key Derivation Function (KDF)
- provides: EC session key randomization; PQ session key randomization; Symmetric ratchet; ext2 randomization
- requires: PRF-ODH reduction
- uses: FIPS-driven component ordering; HKDF.Expand label rule; HKDF.Extract label rule; HMAC; HMAC-SHA256; SHA-384

## Monero  [concept_monero]  (system; 16 papers)
Monero adopts the CryptoNote stealth-address algorithm as part of its core protocol, with the stated goal of unlinkable payments. The chunk says it also hides payer and transaction amount using linkable ring signatures and Pedersen commitments.
Papers: 2018_liu_keyinsulatedstealth, 2020_abraham_blinder, 2020_alonso_zerotomonero, 2020_minaei_moneymorph, 2020_yu_stealthschemes, 2021_monero_mrl73_viewtags, 2021_tabatabaee_mwdos, 2022_monero_pr8061_viewtags
- implements: Tagged output key; View tag
- instance_of: Connection reset attack; Graylist attack; UTXO Model; Whitelist attack
- measures: Monero address and payload sizes; Monero sibling transaction prevalence
- provides: Monero capacity and fee; Payer and amount privacy
- uses: Concise Linkable Spontaneous Anonymous Group (CLSAG); Dandelion++; Incoming viewing keys; Linkable ring signature; Monero signature encoding; Pedersen commitment; Ring signature; Stealth Address; Tags for double-spend prevention; View tag

## Rate-Limiting Nullifier  [concept_rate_limiting_nullifier]  (primitive; 14 papers)
Waku Relay proposes using Rate Limiting Nullifiers for economic spam resistance: peers must stay within a system-defined message rate per epoch or face financial penalties. This is described as an aim, with details delegated to 17/WAKU2-RLN-RELAY.
Papers: 2020_vac_waku2_relay_spec, 2020_vac_waku2_spec, 2022_taheri_spam_protected_gossip, 2022_vac_rln_v1_spec, 2023_signal_pqxdh_spec, 2024_brandt_kt_sok, 2024_cornelius_waku_network_dapps, 2024_revuelta_waku_latency
- defends_against: Balance inflation attack; Eclipse Attack; Invalid-message scoring; Message flooding; On-chain publisher registration; Parallel spend attack; Sybil Attack
- extends: RLN-Diff; RLN-Same; Waku Relay
- implements: Economic spam penalty; Proof fields attached to messages
- improves_on: RLN-V1
- measures: Proof generation cost; Proof verification cost; RLN proof generation and verification latency
- provides: Per-identity gasless quota
- requires: CRH-based Merkle tree; Commitment synchronization; Local RLN membership tree; Mandatory group registration; Maximum epoch gap; Membership tree; On-chain publisher registration
- uses: Groth-16 circuit implementation; Registration, signaling, verification and slashing; Shamir secret sharing; Zero-Knowledge Proof; zk-SNARK

## Authenticated Encryption  [concept_authenticated_encryption]  (primitive; 18 papers)
The symmetric scheme encrypts plaintexts to ciphertexts and decrypts invalid ciphertexts to ⊥. It must be one-time INT-CTXT and IND-CPA secure; honest participants almost surely encrypt only once per key, while adversaries may make many adaptive chosen-ciphertext queries per key.
Papers: 2016_angel_pung_1, 2016_hopwood_zcash_protocol_spec, 2016_kwon_riffle, 2017_alexopoulos_mcmix, 2017_grubbs_franking, 2018_bhargavan_treekem, 2020_abraham_blinder, 2020_bellare_imessage_signcryption
- defends_against: Server denial of service
- implements: IND-CCA2
- provides: Ciphertext integrity; LWPubSub; Message confidentiality; pSaber.PKEhy ANO-CCA reduction bound

## Express  [concept_express]  (system; 12 papers)
An anonymous mailbox communication system using DPFs for efficient write requests and a two-server deployment. It is not designed to withstand active server attacks in broadcast applications; Spectrum is 4–7× faster for 100 kB to 5 MB one-channel messages and has about 70 B request overhead, roughly 75× smaller.
Papers: 2020_abraham_blinder, 2021_2pps_pubsubprivacy, 2021_eskandarian_express, 2022_newman_spectrum, 2023_sasy_sokmetadata, 2024_coijanovic_pirates, 2024_rosenberg_zipnet, 2024_tovey_distributedpir
- assumes: Two-server trust model
- compares_with: Pepper; Pung; Riposte; Single-server latency result; Vuvuzela
- contradicts: End-to-End Unlinkability (EE-UL)
- extends: Riposte; SecureDrop
- implements: Mailbox server storage layout
- instance_of: Compression costs
- measures: Audit client savings; Bandwidth savings; Client cost per message; Operating cost savings; Quadratic scalability; Write complexity
- proves: Soundness
- provides: Asynchronous reads and writes; MAC-based message integrity; Round-independent cryptographic privacy; Symmetric cryptography only; Throughput and latency
- requires: Rogue server and clients threat model
- uses: Auditing protocol; Dialing via public broadcast; Distributed Point Function; Distributed point functions; Dummy-write cover traffic; Express mailbox addressing cost; Fixed-size message padding; Mailbox key shares; Rerandomized mailbox encryption; SNIP

## Key encapsulation mechanism  [concept_kem]  (primitive; 14 papers)
A KEM consists of key generation, encapsulation and decapsulation, producing a ciphertext and symmetric key; the paper requires strong correctness for its stated eSM correctness result. Strong correctness demands decapsulation recover the key for every encapsulation randomness.
Papers: 2022_cremers_pq_secure_messaging, 2022_ishibashi_pq_osake, 2023_beguinet_tamarin_pqsignal, 2023_stainton_pqsphinx, 2024_bhargavan_pqxdh, 2024_fiedler_pqxdh_analysis, 2024_fiedler_pqxdh_deniability, 2024_rial_outfox
- provides: Anonymous KEM notions; IND-CCA; IND-CPA security; PQ shared secret randomization
- requires: IND-CCA; IND-CCA security; Theorem 4.4 non-deniability bound

## Olm  [concept_olm]  (protocol; 10 papers)
Matrix's pairwise protocol uses a Double Ratchet and Triple Diffie-Hellman (3DH); peers fetch identity and one-time pre-keys from an Olm server. One-time pre-keys are unsigned in the Olm specification, while the Matrix protocol requires them signed.
Papers: 2016_matrix_megolm_spec, 2016_matrix_olm_spec, 2016_ncc_olm_review, 2021_dimeo_sok_multidevice, 2022_blazy_pcs_taxonomy, 2023_albrecht_matrix, 2023_matrix_core_formal, 2024_cremers_pcs_impossibility
- attacks: Olm unknown key-share attack
- compares_with: Signal Protocol
- contradicts: Forward Secrecy; Post-Compromise Security
- extends: Signal Protocol
- implements: Double Ratchet
- improves_on: Ephemeral key signature
- instance_of: Signal Protocol
- part_of: Matrix
- provides: Deniability; Forward Secrecy; Megolm; Olm chain forward secrecy; Post-Compromise Security
- uses: AES-256; Central server key bundle; Curve25519; Curve25519 identity keys; Double Ratchet; Ed25519 identity keys; HKDF; HMAC-SHA-256; Minimal Triple Diffie-Hellman; Olm Triple DH

## Kyber  [concept_kyber]  (protocol; 10 papers)
Kyber is a KEM selected by NIST for standardization in public-key encryption and key establishment. The paper proves post-quantum ANO-CCA security for Kyber in the QROM under MLWE and gives an approach to tight IND-CCA security.
Papers: 2017_bos_kyber, 2022_grubbs_anonrobustpq, 2022_maram_pq_anonymity_kyber, 2022_xagawa_anonymitykems, 2023_cremers_keeping_up_kems, 2023_pu_fuzzystealthsigs, 2024_bhargavan_pqxdh, 2024_fiedler_pqxdh_analysis
- assumes: Module Learning With Errors; Module-LWE; Quantum random oracle model; Random oracle model
- compares_with: Communication versus Ring-LWE; ML-KEM; Quantum random oracle model; Saber
- improves_on: NewHope KEM
- instance_of: ML-KEM; QROM extra-hash proof barrier
- measures: Matrix expansion cost
- motivates: Kyber1024 cost tradeoff
- proves: Additional KEM binding property; Kyber KEM correctness bounds; Semi-honest collision resistance
- provides: ANO-CCA security; IND-CCA; IND-CCA security; IND-CPA security; Key Privacy; LEAK+r KEM binding; Robustness
- requires: Two-decapsulation-oracle simulation obstacle
- uses: Fujisaki–Okamoto transform; Hash public key into pre-key; Implicit rejection; Keccak primitive suite; Kyber.CPA; Nested ciphertext hash; Quasar; Recommended parameters k=3; Short-term parameters k=2

## Fujisaki–Okamoto transform  [concept_fujisaki_okamoto_transform]  (mechanism; 15 papers)
Kyber constructs its KEM from a base PKE by applying a tweaked FO transform. The transform hashes the message, derives coins and keys, verifies re-encryption, and implicitly rejects with a secret fallback value.
Papers: 2017_bos_kyber, 2018_bindel_hybrid_kem_ake, 2018_giacon_kem_combiners, 2019_brendel_pq_x3dh, 2019_stebila_rfc9954_hybridtls, 2022_grubbs_anonrobustpq, 2022_maram_pq_anonymity_kyber, 2022_xagawa_anonymitykems
- compares_with: Bounded-depth UPIBE
- contradicts: FO transform open question
- defends_against: Key reuse attacks
- extends: FO6 variant results
- improves_on: Standard KEM; XOR core
- proves: IND-CCA
- provides: CKAKEM; Chosen-ciphertext attack; IND-CCA; IND-CCA2; Implicit rejection
- requires: Parallel ciphertext FO handling; Random oracle model
- uses: Explicit rejection; HU transform variants; Implicit rejection; One-Way To Hiding Lemma; Transform T; U transform variants

## Atom  [concept_atom]  (system; 10 papers)
Atom uses random permutation networks to mix packets. Atom #1 verifiably shuffles and broadcasts proofs, aborting on a discrepancy; Atom #2 uses threshold cryptography, tolerates some drops at a privacy cost, and guarantees only k-anonymity.
Papers: 2017_kwon_atom, 2018_lazar_karaoke, 2019_ando_complexity, 2020_kwon_xrd, 2021_eskandarian_express, 2023_langowski_trellis, 2023_sasy_sokmetadata, 2026_davitt_mixnetusability
- assumes: Anytrust assumption; Manytrust
- compares_with: Alpenhorn; DC-net; Loopix; Mixnet; Riposte; Server bandwidth comparison; Stadium; Tor; Vuvuzela
- contradicts: Stadium and Atom #1 fragility
- defends_against: Traffic Analysis
- hides: Key Privacy
- improves_on: Trap messages
- instance_of: Mixnet
- measures: Dummy message volume; Estimated AWS cost; Mixing latency scaling; One million user latency; Primitive latency; Shuffle proof cost
- proves: Horizontal scalability
- provides: Anonymity Set; Malicious user identification; Server failure tolerance
- requires: Availability attack limit
- uses: Anytrust group; Atom zero-knowledge bottleneck; Dialing mailbox assignment; Dialing message size; Differential Privacy; IND-CCA2; Layer pipelining; Microblog message size; Mixnet; NIZK

## EUF-CMA  [concept_euf_cma]  (property; 14 papers)
An adversary obtains signatures on chosen messages and must forge signatures on distinct, previously unsigned messages; the paper extends the notion to classical and quantum stages and oracle access.
Papers: 2014_syta_dissentanalysis, 2017_bindel_transition_pki, 2020_alwen_mls_insider, 2021_madathil_privatesignaling, 2022_hashimoto_mls_metadata, 2024_argo_pq_signatures_privacy, 2024_bhargavan_pqxdh, 2024_nist_fips205
- assumes: Algebraic Group Model; Random oracle model
- contradicts: Message-bound signature requirement
- proves: ECDSA security bound
- requires: Classical computational security theorem

## IND-CPA security  [concept_ind_cpa]  (property; 17 papers)
In the stated experiment, an adversary observes the encapsulation key, challenge ciphertext, and either its true shared key or a fresh random string, and may create encapsulations. Security means its win probability differs from 1/2 only negligibly; this models passive eavesdroppers.
Papers: 2017_bindel_transition_pki, 2017_bos_kyber, 2018_bindel_hybrid_kem_ake, 2019_stebila_rfc9954_hybridtls, 2020_alwen_mls_insider, 2021_agrawal_lattice_blind_sig, 2021_hashimoto_chained_cmpke, 2021_hashimoto_pq_x3dh_deniable
- assumes: Public-channel exposure
- instance_of: IND-CPA encryption assumption
- measures: Key Encapsulation Mechanism
- proves: Generalized Selective Decryption (GSD)
- requires: Encrypted signing-key embedding; Honest-signer blindness; Negligible distinguishing advantage

## Blockchain  [concept_blockchain]  (system; 14 papers)
A distributed ledger whose multiple nodes store data, providing decentralization, tamper resistance, and no single point of failure. In the proposed architecture it replaces the broker as intermediary, while transaction hashes for sensor, diagnosis, and therapy data are sent through the chain.
Papers: 2018_ramachandran_trinity, 2019_banno_interworking_layer, 2020_albreiki_blockchain_oracles, 2021_abegg_supra, 2021_tian_iot_pubsub_access_control, 2022_alwen_decaf, 2022_dzakie_private_blockchain_mqtt_auth, 2022_tzialla_transparencydictionaries
- defends_against: DDoS attack; Single Point of Failure
- implements: Ledger Event Storage
- improves_on: Access Control List (ACL)
- leaks: Public transaction visibility
- provides: Anonymity; Decentralized consensus DoS claim; Distributed Ledger; Distributed authentication service; Smart Contract; Tamper-proof policy integrity; Trust-boundary persistence ordering immutability
- requires: Consensus Protocol
- uses: Public-key encryption

## PolderCast  [concept_poldercast]  (system; 9 papers)
PolderCast uses an epidemic algorithm to build topic-specific subscriber rings with extra random links to speed propagation in large rings and address churn-related partitions. Publishers must also subscribe, so forwarding involves interested nodes.
Papers: 2012_setty_poldercast, 2014_chen_overlay_network, 2019_araujo_communication_causal, 2019_vyzovitis_gossipsub_v01, 2019_wael_improve, 2020_savolainen_streamr_network, 2021_antunes_pulsarcast, 2022_zaarour_openpubsub_supporting
- compares_with: Millions-node scale target; Scribe churn miss ratio; Scribe delay ratio; Topic-Connected Overlay; VCube-PS single-copy delivery
- extends: Geography-aware vicinity selection
- implements: Three gossip modules; Three-layer architecture
- instance_of: Topic-Based Pub/Sub
- measures: Control-message overhead; Convergence with over 400 topics; Dissemination metrics; Evaluation scale 10K; Evaluation workloads; Facebook workload; PolderCast churn miss ratio; Traffic overhead; Twitter workload
- provides: 99% rings complete within 60 cycles; Cyclon and Vicinity shortcut mix; No privacy or cryptographic mechanism described; Random-shortcut resilience; Static hit ratio; Topic-Connected Overlay
- uses: Churn experiment conditions; Cyclon; Gossip length 10; Gossip-based dissemination; King latency dataset; Peer Sampling; PeerSim; Per-topic bidirectional ring; Proactive dead-neighbor removal; Random shortcut links

## Whisper  [concept_whisper]  (protocol; 13 papers)
Swarm PSS borrows Whisper’s cryptography, envelope structure, and API; Whisper is described as a gossip-based dark messaging system that lacked scalability and wide adoption.
Papers: 2017_eip_627_whisper, 2018_status_whisper_mailserver_spec, 2018_status_whisper_usage_spec, 2019_henningsen_falsefriends, 2019_status_secure_transport_spec, 2019_vac_waku1_spec, 2019_vac_waku_mail_spec, 2020_vac_waku2_message_spec
- extends: Status secure transport layer
- implements: Publish/Subscribe
- instance_of: Publish/Subscribe; Whisper network
- measures: Version 6 implementation status
- motivates: Waku
- provides: Asynchronous operation; Dynamic PoW adjustment; Ignore unsupported packet codes; Offline messaging
- uses: Bloom-filter topic sharing; DEVp2p; Envelope fields; Messages packet; P2P Message packet; P2P Request packet; PoW Requirement packet; Proof of Work; RLP packet encoding; Status packet

## LWE assumption  [concept_lwe]  (assumption; 12 papers)
The lattice-based encryption setting used by SimplePIR and for compact selection-vector queries. The paper gives typical secret dimension N≈2^10 and discusses public matrix A of size about N log₂q relative to the query index.
Papers: 2018_ling_lattice_group_sig, 2021_liu_omr, 2023_beullens_lattice_blind_sig, 2023_li_hintlesspir, 2023_liu_gomr, 2023_pu_fuzzystealthsigs, 2024_collins_dr_tight, 2024_collins_k_waay
- assumes: Ring-LWE; Worst-case lattice hardness basis
- proves: Shortest Vector Problem (SVP); Snake-eye resistance
- provides: CKAKEM; Extended-LWE reduction
- uses: FrodoKEM; Random oracle simulation

## Chord  [concept_chord]  (protocol; 13 papers)
A variant of Chord provides the mapping from clique keys to clique members. The text treats Chord security separately and notes that repeated lookups from different ring starting points make subversion difficult due to redundant routing information.
Papers: 2003_goel_herbivore, 2012_li_sybilcontrol, 2013_ciancaglini_keybased, 2014_pellegrino_pushingdynamic, 2015_kermarrec_want_centralized, 2015_roos_impossibility_self_stabilization, 2016_royer_content, 2016_royer_routagebase
- assumes: Topology security boundary
- implements: Chord membership updates
- instance_of: Distributed Hash Table
- measures: Chord lookup hops; churn overhead simulation result
- provides: Chord routing table; Degraded Chord routing; Peer notification brokers; Receiver discovery
- uses: Chord key hashing; Chord successor routing

## Diffie-Hellman  [concept_diffie_hellman]  (primitive; 15 papers)
LotusNet can use distributed storage for a preliminary Diffie–Hellman exchange to establish a secure out-of-band connection. The resulting channel is authenticated and encrypted because key agreement occurs over an authenticated layer.
Papers: 2009_danezis_sphinx, 2012_mulamba_design, 2015_zhang_tor_quantum_handshake, 2016_cohngordon_pcs, 2016_lazar_alpenhorn, 2018_unger_deniable, 2019_bhargavan_mls_formal, 2019_brendel_pq_x3dh
- implements: X3DH
- motivates: Split KEM
- provides: Diffie–Hellman shared-secret label
- uses: Asynchronous Ratchet Tree (ART)

## ElGamal encryption  [concept_elgamal]  (primitive; 15 papers)
VSM uses signed, CCA ElGamal encryption for UNS candidates and threshold ElGamal for homomorphic operations, rerandomization, and PETs. The ElGamal SMPP variant avoids trusted setup beyond the bulletin board and threshold decryption but uses more expensive NIZKs.
Papers: 2012_wolinsky_dissentnumbers, 2016_kwon_riffle, 2017_chaum_cmix, 2017_kwon_atom, 2017_shirazi_multiparty, 2018_unger_deniable, 2019_chase_signal_private_groups, 2021_duguey_thesis
- implements: urPKEEG
- instance_of: Verifiable shuffle cost
- provides: Rerandomizable key-indistinguishable encryption
- requires: Diffie-Hellman hardness
- uses: Verifiable shuffle

## Global passive adversary  [concept_global_passive_adversary]  (actor; 14 papers)
The analysis considers an observer able to collect all slices and detect communicating DC groups and their broadcast message, but unable to identify a sender within the group under the protocol's traffic-equalization condition.
Papers: 2016_hayes_tasp, 2017_das_trilemma, 2017_piotrowska_loopix, 2020_kuhn_sokperformance, 2021_modinger_k_anonymous_dc, 2024_benguirat_betamixing, 2024_rahimi_larmix, 2025_mavroudis_llmix
- assumes: Global traffic visibility; Group k-anonymity
- attacks: FIFO ordering; Mixnet; Pairwise unlinkability; Third-party sender-receiver unlinkability; Traffic Analysis; User unlinkability
- leaks: Propagation delay
- measures: Geometric target output position
- uses: Global observation assumption

## Privacy Pass  [concept_privacy_pass]  (protocol; 9 papers)
Anonymous tokens for distinguishing honest from malicious CDN requests without relying on IP reputation; PMBTokens extends it with a private metadata bit. Its reported Ristretto/Curve25519 issuance and redemption times are 303 µs and 95 µs.
Papers: 2018_davidson_privacypass, 2020_kreuter_anontokens, 2023_policharla_pq_privacy_pass, 2023_rfc9497_oprf, 2024_rfc9576_privacypass_arch, 2024_rfc9577_privacypass_httpauth, 2024_rfc9578_privacypass_issuance, 2025_chairattana_everlasting_tokens
- assumes: One-more ElGamal decryption security
- compares_with: Everlasting Anonymous Rate-Limited Tokens (EARLT)
- implements: Blind token signing; Token redemption
- instance_of: Anonymous Credentials; Cloudflare browser deployment
- measures: Added upload time
- motivates: Batched evaluation
- proves: Privacy Pass 1-unlinkability; Privacy Pass one-more unforgeability bound
- provides: Anonymous whitelisting use; Binary issuance media types; Blind RSA issuance test vectors; Blindness; Challenge reduction factor; One-more-token security; Privacy Pass 1-unlinkability; Privacy Pass deterministic tokens; VOPRF issuance test vectors
- requires: Privacy Pass Architecture
- uses: Blind RSA; Blind issuing of attributes; Issuance protocol; Oblivious pseudorandom function (OPRF); Redemption protocol; VOPRF construction

## Sender Keys  [concept_sender_keys]  (protocol; 6 papers)
Group messaging without group key agreement: each peer distributes a sender public key and ratchet key over a secure peer-to-peer channel. Receivers store other peers' sessions; the protocol provides confidentiality, forward secrecy, and authentication under that secure-channel assumption, but not transcript equivalence.
Papers: 2023_balbas_sender_keys, 2024_jaeger_keybase_signcryption, 2024_matrix_symbolic, 2025_albrecht_whatsapp_multidevice, 2025_collins_gurke, 2026_gegenhuber_sendandpretend
- assumes: Abstract message terms; Central ordering assumption; Finite group peers; Perfect message ordering
- attacks: Authentication forward-security attack; Randomness exposure and manipulation
- compares_with: Double Ratchet; MLS
- contradicts: Group membership security; Transcript equivalence
- extends: Sender Key consistency rules; Sender Keys+; Signal Protocol
- implements: Sender key chain and per-message keys
- instance_of: Matrix; S-SSMR setting; Signal Protocol
- leaks: Exposure reveals challenge message key; No cryptographic group binding; Passive eavesdropping after update; Sender Key Exposure Weaknesses
- measures: Group operation communication costs; Sender Key Membership Costs
- part_of: Signal v2 groups
- provides: Added-member message access; Forward Secrecy; Limited post-compromise security; Per-member key state; Post-Compromise Security; Practical group size; Weak PCS healing
- requires: Group change rekey; Membership enforcement uncertainty; Pairwise channels for distributing keys; Two-party channel healing condition
- uses: AES-CBC; Key rotation; Per-message chain-key ratchet; Pseudorandom generator; Sender Keys session; Sender Keys session state; Sender signatures; Signal Protocol; Signed control messages; Skipped-message key cache

## Falcon  [concept_falcon]  (system; 7 papers)
Lattice-based NIST candidate based on NTRU. Falcon 512 (Level 1) and 1024 (Level 5) have 897/1793-byte public keys and 690/1330-byte signatures; floating-point hardware optimizations can improve signing by about 20 times.
Papers: 2020_fouque_falcon_spec, 2020_sikeridis_pq_tls_performance, 2021_agrawal_lattice_blind_sig, 2021_hashimoto_pq_x3dh_deniable, 2024_juaristi_pq_ethereum, 2025_berger_pq_tor, 2025_katsumata_deniability_analysis
- assumes: Implementation constraints
- attacks: Lattice reduction
- defends_against: Hybrid attack; Overstretched NTRU attack
- improves_on: Unoptimized PQ implementations
- instance_of: Dilithium and Falcon time-sensitive choice; GPV framework; NIST post-quantum standardization competition
- measures: Key-generation benchmark; Second transcript size; Signature performance; Signing and verification benchmark; Signing throughput
- motivates: Compactness objective
- provides: Falcon-1024 parameters; Falcon-512 parameters; Key-recovery mode; PQ certificate-chain growth; Signature generation; Signature verification
- requires: Key management overhead; Modulus q; Ring degrees; Signature standard deviation; Signature tailcut
- uses: Babai reduction; Binary64 floating point; FFT implementation; Falcon tree; Fast Fourier sampling; GPV framework; Iterative key-generation memory tradeoff; Key-generation filtering; LDL tree construction; NTRU lattices

## ML-DSA  [concept_ml_dsa]  (protocol; 8 papers)
NIST’s module-lattice-based digital signature algorithm, based on Module Learning With Errors. It specifies key generation, signing, and verification, with three approved parameter sets of different security strengths.
Papers: 2024_nist_fips204, 2024_nist_ir8547_transition, 2025_berger_pq_tor, 2025_driscoll_rfc9794, 2025_rfc9794_pqt_hybrid_terminology, 2025_tian_mls_pqcombiner, 2025_zhaisenbayev_ilyazh_web3e2e, 2026_mallick_aquaman
- assumes: MLWE assumption; SelfTargetMSIS assumption
- instance_of: Post-quantum asymmetric cryptographic algorithm
- measures: Certificate chain size; Expected signing repetitions; Key and signature sizes
- motivates: PQC overhead estimate
- provides: Claimed security categories; Deterministic signing; Digital signature properties; Hedged signing; Key generation, signing, and verification; Signature and signed data delivery; Strong existential unforgeability; Strong unforgeability claim; Three approved parameter sets
- requires: Context-string bound; Destroy sensitive intermediate data; Key management overhead; Key-generation seed ξ; No floating-point arithmetic; Signature and public-key length checks
- uses: Compressed public value t1; Fiat–Shamir with Aborts; Hashed message representative; Hashed rounded commitment; Module-structured matrices; Public seed for matrix derivation; SHAKE128 and SHAKE256; Signature hint; Signature key roles

## Continuous Group Key Agreement (CGKA)  [concept_continuous_group_key_agreement]  (primitive; 10 papers)
CGKA requires correctness so all members output the same keys in every epoch, key privacy, and post-compromise forward secrecy. Its security game lets the adversary control group operations, leak party state at any time, and guess whether a challenged epoch key is real or random, subject to a safety predicate.
Papers: 2019_alwen_tainted_treekem, 2021_alwen_key_grafting, 2021_alwen_server_aided_cgka, 2022_alwen_cocoa, 2022_balbas_a_cgka, 2023_auerbach_pcs_cost_concurrent, 2023_chevalier_quarantined_treekem, 2025_auerbach_cgka_no_pruning
- assumes: Asynchronous server setting; Authenticated-channel assumption
- attacks: CGKA leakage and no-delete attacks
- extends: Double Ratchet
- instance_of: TreeKEM
- provides: Forward Secrecy; Forward secrecy goal; MLS; Messaging Layer Security (MLS); Post-Compromise Security; Post-compromise forward security (PCFS)
- requires: Disjoint symbolic random coins; No distributed work; No nested encryption; OW-k-PCS¬RC security
- uses: CGKA history graph; CGKA init-key registration; Key-derivation graph; Propose-and-commit paradigm; Symbolic entailment model; TreeKEM

## Homomorphic encryption  [concept_homomorphic_encryption]  (primitive; 12 papers)
A symmetric-key encryption scheme over vectors in Z_p^m supports evaluating an encrypted public inner product and returning a ciphertext decrypting to that product. The defined correctness probabilities exceed 1−negl(λ) for direct decryption and evaluation.
Papers: 2013_boutet_decentralizing, 2013_yoon_adaptation_techniques, 2015_decouchant_collusions, 2016_jakobsen_bootstrap_anonymous, 2016_jansen_safely_measuring_tor, 2019_ali_pircommcomp, 2022_fleischhacker_compressencrypted, 2022_jin_secure
- compares_with: Decentralized user-based collaborative filtering
- defends_against: Publication Confidentiality
- implements: Publish/Subscribe
- uses: Learning with Errors

## Shamir secret sharing  [concept_shamir_secret_sharing]  (primitive; 12 papers)
A degree-(t−1) polynomial over Fq shares one secret among N auditors; any t shares reconstruct, while the text states perfect t-privacy for uniform independent coefficients. The field must satisfy q > 2^512 to embed the 512-bit secret directly.
Papers: 2013_yoon_adaptation_techniques, 2019_lu_asynchromix, 2019_sonnino_coconut, 2020_abraham_blinder, 2022_shirali_dcnetsurvey, 2022_taheri_waku_rln_relay, 2022_vac_rln_v1_spec, 2024_cho_algebraicbroadcast
- contradicts: Robustness
- implements: Replica threshold scheme; Shared-Dining threshold
- motivates: Authority set change setup

## First-Spy Estimator  [concept_first_spy_estimator]  (attack; 13 papers)
The adversary predicts that the first non-curious node to contact the curious set is the source. Its success probability supplies a lower bound on ε; the proof applies this reasoning to both average-case and worst-case adversaries.
Papers: 2014_bensasson_zerocash, 2015_fanti_hidingrumor, 2017_das_trilemma, 2018_fanti_dandelionpp, 2018_naumenko_erlay, 2020_das_comprehensivetrilemma, 2021_diaz_nym, 2021_franzoni_clover
- assumes: Passive observation model
- attacks: Onion Routing; Recipient anonymity invariant 2; Statistical transaction hiding
- measures: Clover overall precision; Diffusion precision; Precision and recall; Private-spy success rate; Public-spy success rate
- proves: Spy detection floor; Universal ε lower bound

## Website Fingerprinting  [concept_website_fingerprinting]  (attack; 10 papers)
The attack classifies encrypted browsing traffic as a monitored page or website. Page-level classification does not scale across the tested universe, while website-level classification is more effective in the open-world evaluation.
Papers: 2014_juarez_critical, 2015_kwon_circuitfp, 2016_juarez_wtfpad, 2016_panchenko_wfinternet, 2017_kim_sgxtor, 2018_rimmer_automatedwf, 2019_bhat_varcnn, 2020_rahman_tiktok
- assumes: Balanced open-world evaluation; Closed-world assumption
- attacks: Equal Length Packet Splitting; Tor; WTF-PAD
- compares_with: CUMUL
- instance_of: Timing information attack; Traffic Analysis
- leaks: Website visit inference
- measures: Open-world evaluation dataset; Precision; Recall; Website fingerprinting results
- uses: Client-link observation; Cross-entropy confidence threshold; Deep neural network (DNN); Open-world evaluation; Traffic trace features; Website fingerprint training

## Ring signature  [concept_ring_signature]  (primitive; 9 papers)
Monero uses ring signatures to hide links between mints and spends; the discussion names CLSAG and earlier MLSAG. The incoming-key theorem with off-chain channels reduces to chosen-target linkable anonymity of CLSAG.
Papers: 2013_vansaberhagen_cryptonote, 2018_liu_keyinsulatedstealth, 2018_unger_deniable, 2019_chase_signal_private_groups, 2021_brendel_pq_deniable_ake, 2021_hashimoto_pq_x3dh_deniable, 2025_gajland_shadowfax, 2025_hashimoto_bundled_ake
- assumes: Discrete logarithm hardness
- compares_with: Derived-key privacy
- extends: Linkable ring signature; Traceable ring signature
- implements: Attribute-Based Encryption
- instance_of: 2-user ring signature
- leaks: Ring anonymity omitted
- provides: Anonymity against full key exposure; Deniability; MC-Ano; Multi-challenge ring-signature anonymity; UF-CRA1; UF-CRA1 unforgeability; Unforgeability with respect to insider corruption
- requires: Polynomial ring size; SoK zero knowledge assumption

## Verifiable Random Function (VRF)  [concept_verifiable_random_function]  (primitive; 11 papers)
A function with pseudorandom outputs and proofs of correct evaluation. SASSI composes two VRF levels: threshold issuance binds the first output to the identity string; the second produces context-specific pseudonyms.
Papers: 2021_diaz_nym, 2022_chen_rotatable_zks, 2023_ma_verasel, 2023_malvai_parakeet, 2024_brorsson_consistency_or_die, 2024_diaz_reliability, 2024_len_elektra, 2026_jarecki_x3dh_sas
- contradicts: Deniable Authentication
- hides: Auditor leakage
- provides: Key Privacy; Public measurement verification; VRF-output purge bound
- requires: Cryptographic-data pruning; Layered random routing topology
- uses: Rotatable Zero Knowledge Set

## Hashcash  [concept_hashcash]  (protocol; 12 papers)
A proof-of-work system requiring a sender to produce a string whose cryptographic hash begins with a specified number of zeroes. Its solution is expensive to find but comparatively cheap to verify.
Papers: 2002_back_hashcash, 2004_laurie_proofofwork, 2006_liu_pow, 2015_schaub_bitmessage_antispam, 2016_biryukov_equihash, 2018_aggarwal_quantum_bitcoin, 2018_davidson_privacypass, 2020_abraham_blinder
- attacks: Grover search
- compares_with: Proof of Work
- defends_against: Denial of service attack
- improves_on: Verification cost
- instance_of: Impossibility result; Proof of Work; Proportional reward; Unbounded probabilistic cost
- provides: Proof of Work; Publicly auditable cost-function; Six confirmations; Trapdoor-free cost-function; Verification cost
- requires: Spent-token database
- uses: Partial hash collision; SHA-256; Service-name binding

## SHA-256  [concept_sha_256]  (primitive; 12 papers)
Zcash uses full SHA-256 to instantiate NoteCommitmentSprout; its interface maps byte sequences of length N to 32 bytes. SHA256Compress, a single 512-bit block without padding, instantiates several PRFs and MerkleCRHSprout.
Papers: 2016_hopwood_zcash_protocol_spec, 2018_giacon_kem_combiners, 2019_bernstein_sphincsplus, 2020_vac_waku2_message_spec, 2022_albrecht_telegram, 2022_hagen_contactdiscovery, 2022_yin_hdwalletstealth, 2024_jaeger_keybase_signcryption
- uses: SHACAL-2

## Brakerski/Fan-Vercauteren (BFV)  [concept_bfv]  (primitive; 9 papers)
A lattice-based SHE scheme over R = Z[x]/(x^n+1), with ciphertexts containing two polynomials modulo q. Homomorphic additions have additive noise growth; plaintext-ciphertext and ciphertext-ciphertext multiplications grow noise multiplicatively.
Papers: 2021_ahmad_addra, 2021_liu_omr, 2023_ahmad_pantheon, 2023_liu_gomr, 2024_lee_sophomr, 2024_liu_perfomr, 2024_liu_snakeeye, 2025_chen_onionpirv2
- assumes: Learning with Errors; Ring learning with errors; Ring-LWE
- instance_of: Fully homomorphic encryption (FHE)
- provides: Multiply; Noise growth
- requires: BFV noise budget

## SpiderCast  [concept_spidercast]  (protocol; 12 papers)
A system that keeps topic-specific contacts to maintain low average node degree with many subscriptions per node; the text says wildcard subscriptions are not natively supported and would increase degree or contact requirements.
Papers: 2012_li_community_clustering, 2012_olteanu_robust_peer, 2012_setty_poldercast, 2013_boutet_decentralizing, 2013_matos_scaling_up, 2013_mega_social_overlays, 2014_chen_overlay_network, 2016_chen_overlay_design
- compares_with: KATT; PolderCast
- extends: SpiderCastM
- improves_on: Topic overlay maintenance cost
- instance_of: Publish/Subscribe; Topic-Based Pub/Sub
- provides: Five percent membership knowledge; No topic service differentiation; Publish/Subscribe; Topic-Connected Overlay; Traffic confinement steps
- requires: Adjacent-node link coordination; Incomplete candidate similarity degradation
- uses: Correlated subscriptions; Peer Sampling; Social graph clustering; SpiderCast k-coverage stopping rule; Topic-based grouping

## Distributed Point Function  [concept_distributed_point_function]  (primitive; 10 papers)
A DPF lets a client split a point function into two shares that individually reveal nothing about target index or message and whose sum evaluates to the point function. For security parameter λ, shares are O(λ log N + |m|) bits; instantiated with a PRF, write communication is O(λ log N + log |F|) bits.
Papers: 2015_corrigangibbs_riposte, 2018_demmler_pirpsi, 2019_corrigangibbs_sublinear_pir, 2020_abraham_blinder, 2021_2pps_pubsubprivacy, 2021_eskandarian_express, 2022_newman_spectrum, 2023_eskandarian_abusereporting
- assumes: Decision Diffie-Hellman
- compares_with: Private Information Retrieval
- extends: Sparse distributed point functions
- hides: Channel privacy until aggregation
- improves_on: VDPF token overhead
- provides: DPF query size; DPF share communication cost; Multi-server DPF key size; Sublinear data transfer; Two-server DPF key size; Write-private database scheme
- requires: Pseudorandom generator

## Hierarchical identity-based encryption (HIBE)  [concept_hierarchical_identity_based_encryption]  (primitive; 11 papers)
A HIBE can generically instantiate a key-updatable KEM by treating each associated-data update as descent to a lower hierarchy level. The construction in Figure 2 makes an initial descent at setup when the HIBE cannot encapsulate to its root.
Papers: 2018_poettering_asynchronous_rke, 2020_bienstock_group_ratcheting_concurrency, 2022_yin_hdwalletstealth, 2023_alwen_fork_resilient, 2023_rosler_upibe, 2025_collins_gurke, 2025_collins_leakage_rke, 2025_denison_katt
- compares_with: Single-strand secret-key updates
- provides: Forward Secrecy; Identity subtree decryption scope
- requires: IND-CCA security for HIBE

## Key Derivation Function (KDF)  [concept_key_derivation_function]  (primitive; 12 papers)
Protocol-specific KDFs turn key-agreement shared secrets and additional inputs into symmetric encryption keys. Sprout includes output index, hSig, ephemeral public key, and recipient transmission key; Sapling and Orchard use shared secret and ephemeral public key.
Papers: 2012_libert_anonymousbe, 2016_hopwood_zcash_protocol_spec, 2021_duguey_thesis, 2021_javani_aot, 2022_ishibashi_pq_osake, 2023_kocaogullar_pudding, 2024_fiedler_pqxdh_analysis, 2025_auerbach_pq_metric
- assumes: Pseudorandom function
- instance_of: HKDF
- proves: Joiner secret secrecy relation
- provides: Authenticated Encryption
- requires: Collision Resistance; IND-CCA2; PRF-ODH

## Nostr  [concept_nostr]  (protocol; 10 papers)
A decentralized social network launched in 2022, built from open protocols and using relays for post storage and distribution. The study reports over 600 active relays, 9 million users with profiles and contact lists, and 100 million posts in the ecosystem.
Papers: 2020_nip13_pow, 2024_wei_nostr_empirical, 2025_bitchat_protocol_whitepaper, 2025_jeong_dosn_overview, nostr_nip_01, nostr_nip_04, nostr_nip_13, nostr_nip_17
- assumes: Publicly accessible relay sample
- compares_with: P2P community data collection
- implements: Publish/Subscribe
- instance_of: P2P overlay
- leaks: IP address exposure; Public event time
- measures: Six-month dataset window
- provides: Censorship resistance; Event wire fields; Gift wrap (kind 1059); Post replication scale
- requires: Relay availability and fees; Relay availability and financial sustainability
- uses: Client; EC-based Schnorr signature; NIP-44 encryption; NIP-44 version 2; NIP-59 gift-wrapping; Proof of Work; Relay; Relay nodes; SHA-256; Shared-point X-coordinate secret

## HPKE  [concept_hpke]  (protocol; 5 papers)
Hybrid Public Key Encryption test vectors cover setup modes, key derivation, encryption, and exporter outputs. This chunk includes DHKEM(X25519, HKDF-SHA256), DHKEM(P-256, HKDF-SHA256), HKDF-SHA256 or HKDF-SHA512, and ChaCha20-Poly1305 or AES-128-GCM combinations.
Papers: 2022_barnes_rfc9180, 2025_lebrun_thesis, 2025_wallez_thesis, 2025_wallez_treekem_verified, 2026_mangipudi_auditable_cgka
- assumes: Downgrade exposure
- attacks: Key-compromise impersonation (KCI)
- contradicts: Forward Secrecy
- implements: MLS; Simplified HPKE Base-mode model
- leaks: Plaintext length leakage
- part_of: Authenticated modes (PSK, Auth, AuthPSK); Base mode
- proves: Auth mode security bounds; Base mode analysis; Mode security results
- provides: Auth PSK mode; Auth mode; Base mode; Bidirectional key derivation by export; Encapsulation output; HPKE errors; PSK mode; Post-quantum Auth mode; Replay protection limit; Security goals
- requires: AEAD security requirement; Application input limits; KDF security level; KEM key reuse rules; KEM shared secret requirement; Message ordering requirement; PSK entropy requirement; Public key validation
- uses: AEAD options; AES-128-GCM; Associated data; Auxiliary authenticated information; ChaCha20-Poly1305; DHKEM; DHKEM curve options; Domain Separation; HKDF; KDF options

## HintlessPIR  [concept_hintlesspir]  (protocol; 5 papers)
A hintless single-server PIR scheme with no client-dependent preprocessed server state or database-dependent preprocessed client state. Its query is 323KB in the general description, including two compressed ciphertexts and a compressed rotation key; measured table queries range from 334KB to 1502KB.
Papers: 2023_li_hintlesspir, 2024_burton_respire, 2024_decastro_whispir, 2024_menon_ypir, 2025_mahdavi_inspire
- assumes: Initial-query latency model; Random oracle simulation; Single-server setting
- compares_with: DoublePIR; Large-record throughput comparison; Password check cost; SimplePIR; Spiral PIR; Tiptoe PIR
- defends_against: Client hint storage burden; Hint refresh overhead
- extends: LWEPIR; SimplePIR
- hides: Private Information Retrieval
- improves_on: SimplePIR; Spiral PIR; Tiptoe PIR
- instance_of: HintlessPIR comparison; Private Information Retrieval; Single-Server Linear PIR with Preprocessing; Single-server PIR
- measures: Client recovery costs; Hint amortization crossover; Hint download equivalent query cost; HintlessPIR 8.5GB benchmark; HintlessPIR benchmarks; HintlessPIR communication costs; HintlessPIR costs; NTTlessPIR query size; Rotation generation cost; Server online costs
- provides: Few-query advantage; HintlessPIR communication complexity; No client database state; No offline interaction; No server client-dependent state; Response size scaling
- uses: Homomorphic Encryption with Composable Preprocessing; LWE plaintext space; NTTlessPIR; Parallelization mechanism; Reuse public a across fresh keys; Vertical record encoding

## LARMix  [concept_larmix]  (protocol; 5 papers)
Heuristic low-latency routing that favors nearby mixnodes, parameterized by τ: as τ approaches 0 it approaches deterministic closest-node selection, while τ=1 gives uniform routing. The paper reports higher anonymity than MORSE but weaker resilience to strategic corruption than LOR.
Papers: 2024_rahimi_larmix, 2024_rahimi_larmixpp, 2025_rahimi_lamp, 2025_rahimi_malaria, 2026_rahimi_optimix
- assumes: Anonymity Trilemma
- compares_with: Anonymity comparison result; CLAPS; Greedy corruption results; Latency evaluation; Latency reduction result; Mixnode compromise; Nym mixnet size comparison; OptiMix
- defends_against: Fast-node proximity strategy
- extends: Loopix
- hides: Shared routing policy
- leaks: Path entropy limitation
- measures: 150 ms constrained optimum; 8× propagation reduction; Balanced routing result; End-to-end latency decomposition; Hop count measurements; Network size measurements; Network size results; Network size scaling; Route entropy example; Routing complexity
- proves: Adversarial advantage condition
- provides: Entropy latency trade-off; Target latency configuration
- requires: Hourly reconstitution; Load balance condition; VerLoc latency data
- uses: Baseline experiment parameters; Discrete-event simulation; Greedy balancing; Loopix; Naive balancing; RIPE Atlas latency dataset; Routing bias τ; Routing randomness τ; Shared routing policy; Sphinx

## Message authentication code (MAC)  [concept_message_authentication_code]  (primitive; 10 papers)
A MAC consists of signing, which takes key k and message m and outputs tag t, and deterministic verification, which returns true exactly for a valid tag under k. Correctness requires verification of a generated tag to succeed for every key and message.
Papers: 2004_borisov_otr, 2009_goldberg_mpotr, 2017_chaum_cmix, 2018_poettering_asynchronous_rke, 2021_ando_cryptographic_shallots, 2021_duguey_thesis, 2023_balbas_sender_keys, 2024_gregoire_onionfranking
- contradicts: Origin Authentication
- provides: MAC unforgeability; Repudiability; SUF-CMA security
- requires: Strong unforgeability

## Decisional Diffie-Hellman (DDH)  [concept_decisional_diffie_hellman]  (assumption; 13 papers)
DDH assumes no probabilistic polynomial-time algorithm distinguishes (g^x,g^y,g^xy) from (g^x,g^y,g^z) with more than negligible advantage ε. The revised tag and trapdoor proofs rely on its intractability in the random oracle model.
Papers: 2009_danezis_sphinx, 2016_cohngordon_signal, 2019_tyagi_messagefranking, 2019_wang_improving, 2020_kreuter_anontokens, 2022_canetti_uc_messaging, 2023_lazzaretti_treepir, 2023_rosler_upibe
- assumes: DDH unlinkability bound
- implements: DDH hybrid replacement
- provides: Oracle simulation cut

## Public-key encryption  [concept_public_key_encryption]  (primitive; 11 papers)
The construction encrypts the message in its initial protocol and, in the efficient construction, encrypts the witness vectors x and y. The proposed instantiation uses an IND-CPA secure scheme adapted from CRYSTALS-Kyber.
Papers: 2012_libert_anonymousbe, 2018_durak_linear_ratcheting, 2020_bienstock_group_ratcheting_concurrency, 2021_agrawal_lattice_blind_sig, 2022_xagawa_anonymitykems, 2023_auerbach_pcs_cost_concurrent, 2023_beullens_lattice_blind_sig, 2024_hansen_ocash
- provides: AI-CCA; ANON-CCA security; Honest-signer blindness; IND-CCA
- requires: Weak robustness

## Signature scheme (Sig)  [concept_signature_scheme]  (primitive; 10 papers)
Signatures cover Bob's semi-static DH key and KEM key, and may also cover ephemeral KEM keys. Fake needs signatures unknown to the distinguisher for the stated initiator-deniability constructions.
Papers: 2020_alwen_mls_insider, 2020_schwabe_kemtls, 2022_alwen_cocoa, 2022_hashimoto_mls_metadata, 2024_fiedler_pqxdh_deniability, 2024_len_elektra, 2025_collins_gurke, 2025_wallez_treekem_verified
- attacks: Ephemeral KEM signature forgery barrier

## Curve25519  [concept_curve25519]  (primitive; 13 papers)
Curve25519 is the basis for Signal Protocol key generation and exchange; the resulting keys are called X25519 keys. Session also uses X25519 public-private key pairs for user identification.
Papers: 2009_danezis_sphinx, 2013_tor_prop224_rendng, 2015_zhang_tor_quantum_handshake, 2016_hopwood_zcash_protocol_spec, 2016_matrix_olm_spec, 2016_ncc_olm_review, 2020_lobbecke_session_seminar, 2022_thambipillai_streamr_multicast_encryption
- assumes: New generic-group security estimate
- uses: Trusted Execution Environment (TEE)

## Broadcast Encryption  [concept_broadcast_encryption]  (primitive; 12 papers)
Broadcast encryption could optimize encryption for multiple recipients, but the chunk says current schemes are not supported by the JWA stack and require trusted setup for a master secret, conflicting with DIDComm decentralization.
Papers: 2012_bitmessage_wiki_faq, 2016_hopwood_zcash_protocol_spec, 2020_abraham_blinder, 2020_bienstock_group_ratcheting_concurrency, 2020_masinde_peertopeerbased, 2021_duguey_thesis, 2023_liu_gomr, 2023_tessaro_bbs
- compares_with: Fixed GOMR (FGOMR); PKI resource PKI_n
- hides: Sender and receiver hiding claims
- part_of: Allowed lower-bound primitives
- proves: AGM BBS security theorem
- provides: Collusion resistance
- requires: Central administration
- uses: Complete subtree method

## Hyperledger  [concept_hyperledger]  (system; 13 papers)
Hyperledger Fabric is the private blockchain framework used as broker; its chain stores permanent interaction history and channel data. The text says an adversary would need more computation power than all honest participants to change stored information.
Papers: 2018_ramachandran_trinity, 2019_bu_hyperpubsub, 2020_berendea_fabric_gossip, 2020_kim_pbft_openstack_message_queue, 2021_ghaemi_pubsub_interoperability, 2021_kaleem_edsc, 2021_tian_iot_pubsub_access_control, 2023_alam_formal
- assumes: Trusted membership service provider
- implements: Execute order validate
- instance_of: BPAC mechanism; Experimental setup; Permissioned Blockchain
- provides: Publish/Subscribe
- uses: BBS+ signatures; Infect-and-die push; Pull component; Recovery component

## Mix networks  [concept_mix_network]  (protocol; 11 papers)
A message-routing architecture that relays traffic through mix servers to obscure sender-recipient correspondences. Loopix applies it in a stratified topology and uses independent paths for each message.
Papers: 2013_zamani_anonymousbroadcast, 2016_galteland_cmixattacks, 2017_piotrowska_loopix, 2020_kuhn_sokperformance, 2022_shirali_dcnetsurvey, 2024_rahimi_larmix, 2024_scherer_sphinxproof, 2025_mavroudis_llmix
- assumes: Global passive adversary; Mixnode adversary
- defends_against: Global adversary
- instance_of: Loopix; Nym
- leaks: Traffic Analysis
- motivates: Tor
- provides: Honest node preserves privacy; Sender-Receiver Unlinkability
- uses: Dummy Messages; Dummy messages; Sphinx

## Learning with Errors  [concept_learning_with_errors]  (assumption; 9 papers)
FrodoPIR's security is based on decisional ternary LWE, with secret and error entries sampled uniformly from {−1,0,1}. The chunk states hardness follows from standard worst-case lattice problems for appropriate parameters, against classical and quantum adversaries.
Papers: 2022_corrigangibbs_pirsublinearamortized, 2022_davidson_frodopir, 2022_henzinger_simplepir, 2022_lazzaretti_nearoptimalpir, 2024_celi_keywordpir, 2024_lee_sophomr, 2024_menon_ypir, 2025_chen_onionpirv2
- requires: mmKEM1 construction
- uses: 128-bit security parameters

## Oblivious Transfer  [concept_oblivious_transfer]  (protocol; 11 papers)
Basic OT lets a sender transfer one of two messages selected by the receiver without learning the selection; the receiver learns only the selected message. A small number such as 128 base OTs can be extended using symmetric cryptography.
Papers: 2004_boneh_peks, 2019_kales_contactdiscovery, 2020_vac_waku2_filter_spec, 2021_hue_privacyenhanced, 2021_javani_aot, 2021_madathil_privatesignaling, 2021_mazmudar_you, 2022_klingler_confidentialite
- compares_with: Private Information Retrieval
- extends: 1-out-of-2 OT; OT k-out-of-n scheme
- provides: Sender-receiver unlinkability

## RLWE assumption  [concept_rlwe]  (assumption; 10 papers)
Ring Learning With Errors encodings support Respire's query privacy and packed response processing. Security assumes RLWE and key-dependent pseudorandomness for specified function families.
Papers: 2017_polyakov_prepubsub, 2023_abdennebi_latticebased, 2023_li_hintlesspir, 2024_burton_respire, 2024_lee_sophomr, 2024_liu_perfomr, 2025_liang_instantomr, 2025_mahdavi_inspire
- defends_against: Query privacy
- proves: RLWE security parameter example
- requires: Signal key
- uses: RLWE key switching

## Zenoh  [concept_zenoh]  (system; 6 papers)
An edge-native data fabric for heterogeneous Edge environments and asymmetric systems, including devices that may sleep. It routes data represented as (name, value) pairs without requiring prior infrastructure knowledge and has a stated minimum wire overhead of 5 bytes.
Papers: 2021_baldoni_zenohdataflow, 2023_liang_zenohperformance, 2024_chovet_performancecomparison, 2024_mehran_runtimeverification, 2025_kluner_zenohautomotive, 2026_paul_benchmarkingmessage
- improves_on: Topic discovery
- instance_of: Topic-Based Pub/Sub; Zenoh version used
- measures: 1 MB latency results; Multi-machine latency results; Multi-machine throughput results; Single-machine brokered Zenoh throughput; Single-machine latency results; Single-machine throughput results
- provides: Direct peer mode; Discovery overhead reduction; Dynamic discovery; Geo-distributed storage; Minimum wire overhead; Queryable computations; Reliability levels; Transport choices; Wire-level batching
- requires: Zenoh domain ID arrangement
- uses: Publish/Subscribe; Reliable and best-effort modes; Topic and key matching; Topic-Based Pub/Sub; Zenoh reliability settings; Zenoh router

## SimplePIR  [concept_simplepir]  (protocol; 7 papers)
A PIR baseline benchmarked on the same environment. Its hint sizes in Table 1 range from 16MB to 185MB; a pair of HintlessPIR query and response is about 1% of its hint for all measured databases except the smallest.
Papers: 2022_henzinger_simplepir, 2023_li_hintlesspir, 2024_burton_respire, 2024_celi_keywordpir, 2024_decastro_whispir, 2024_menon_ypir, 2025_mahdavi_inspire
- assumes: Learning with Errors
- compares_with: Throughput comparison
- defends_against: Long-term PIR state risk
- improves_on: Generic filter-to-keyword-PIR transformation
- instance_of: Private Information Retrieval
- measures: Batched throughput; PIR throughput results; Packing and rotation count; Per-query cost
- proves: SimplePIR correctness bound; SimplePIR multi-query security; SimplePIR security theorem
- requires: SimplePIR parameter selection
- uses: LWE assumption

## Unlinkability  [concept_unlinkability]  (property; 9 papers)
BACAP box IDs are computationally unlinkable to storage servers without read capabilities; quantum unlinkability relies on KDF output indistinguishability, negligible reduction bias, and roughly 2^256 keyspace enumeration difficulty.
Papers: 2010_pfitzmann_terminology, 2015_barroso_adtn, 2020_kreuter_anontokens, 2020_vac_waku2_message_spec, 2021_vac_waku2_payload_spec, 2023_attarian_mixflow, 2023_kocaogullar_pudding, 2025_infeld_echomix
- assumes: BACAP quantum unlinkability assumptions
- provides: Privacy-enhancing identity management
- requires: Anonymity Set; Loopix

## TreeKEM  [concept_tree_kem]  (protocol; 9 papers)
TreeKEM is cited as a protocol whose security can be upgraded to the stronger server model because round messages contain signed messages and the adversary lacks parties’ signing keys.
Papers: 2020_bienstock_group_ratcheting_concurrency, 2021_hashimoto_chained_cmpke, 2022_alwen_cocoa, 2022_hashimoto_mls_metadata, 2023_alwen_fork_resilient, 2023_chevalier_quarantined_treekem, 2024_chou_bots_groupchats, 2025_lebrun_thesis
- assumes: Sequential update restriction
- compares_with: Static metadata leakage functions
- leaks: Ghost users
- part_of: MLS
- provides: Crypto-agility; Forward Secrecy; Post-Compromise Security; TreeKEM group operations
- requires: Forward Secrecy; Post-Compromise Security
- uses: ML-KEM; Ratchet Tree degree; TreeKEM Ratchet Tree

## Harvest Now, Decrypt Later Attack  [concept_harvest_now_decrypt_later]  (attack; 11 papers)
The adversary stores intercepted encrypted messages and decrypts them later after obtaining a sufficiently powerful quantum computer. PQ3's modeled quantum attacker is passive and starts only after honest participants stop running the protocol.
Papers: 2016_signal_double_ratchet_spec, 2024_apple_pq3, 2024_bhargavan_pqxdh, 2024_fiedler_pqxdh_deniability, 2024_linker_imessage_pq3, 2024_nist_ir8547_transition, 2025_hashimoto_bundled_ake, 2025_session_protocol_v2
- assumes: Quantum-attacker timing assumption
- attacks: Diffie-Hellman; Elliptic curve cryptography; RSA
- requires: Quantum attacker capability
- uses: Third-party ciphertext collection

## Talek  [concept_talek]  (system; 10 papers)
Related work describes Talek as a PIR-based private pub/sub system for protecting many client communications from a small number of untrusted servers. It uses Oblivious Logging and Private Notifications and requires dummy requests when clients have nothing to read or write.
Papers: 2017_tyagi_stadium, 2018_lewis_cwtch, 2020_cheng_talek, 2021_2pps_pubsubprivacy, 2021_eskandarian_express, 2022_klingler_confidentialite, 2023_kocaogullar_pudding, 2023_sasy_sokmetadata
- assumes: Anytrust threat model; Two-server non-collusion assumption
- compares_with: 2PPS; Private Information Retrieval
- contradicts: Availability limitation; Publisher-subscriber decoupling
- instance_of: Publish/Subscribe; Topic-Based Pub/Sub
- leaks: GetUpdates leakage; Online status leakage
- measures: Three-server performance result
- proves: Access sequence indistinguishability
- provides: Access sequence indistinguishability; GPU implementation; Private log abstraction; Talek requirement gaps
- uses: Blocked cuckoo hashing; Bloom Filter; Bounded server storage; Fixed-rate cover requests; Private Information Retrieval; Private notifications

## TLS 1.3  [concept_tls_1_3]  (protocol; 7 papers)
Encrypted tunnel protocol providing integrity, confidentiality, and endpoint authentication. The study evaluates full 1-RTT handshakes without PSK resumption and excludes the TCP handshake from handshake latency.
Papers: 2019_stebila_rfc9954_hybridtls, 2020_schwabe_kemtls, 2020_sikeridis_pq_tls_performance, 2021_simplex_smp_spec, 2024_mattsson_symmetric_ratchets, 2025_wallez_thesis, 2026_draft_act
- attacks: AEAD key/nonce collision attack
- compares_with: Client first application data
- defends_against: Key-share reuse risk
- improves_on: Ephemeral key exchange
- measures: TLS/Signal precomputation security
- provides: Forward Secrecy; TLS traffic-secret space shrink
- requires: Recommended ephemeral rekey interval; Traffic-secret entropy rule
- uses: HKDF-Expand; X.509; ρ-chain

## WhatsApp  [concept_whatsapp]  (system; 6 papers)
The study reports that WhatsApp returns stealth delivery receipts to unknown users and that covert probing can reveal device and activity information. Reaction messages can also be used for traffic and battery exhaustion.
Papers: 2014_coull_imessage_privacy, 2017_rosler_more_is_less, 2021_hagen_contact_discovery, 2024_gegenhuber_careless_whisper, 2025_albrecht_whatsapp_multidevice, 2026_gegenhuber_whatsapp_enumeration
- assumes: Server-controlled group membership
- implements: Contact discovery
- instance_of: Contact-storage tradeoff; Device-Oriented Group Messaging (DOGM); Traffic inflation
- leaks: Packet-size metadata leakage
- measures: Weak practical rate limits
- provides: Arbitrary target probing; Pairwise session store cap; Phone-number contact discovery; Reaction payload limits; Received group session cap; Registrable mobile-number space; Session key bundle; WhatsApp future secrecy failure; WhatsApp single group ciphertext
- uses: Authenticated encryption with associated data; Delivery receipts; Encrypted attachments; History sharing; Identity fingerprint verification; Key Transparency; Multi-device management; Sender Keys; Signal Protocol; Trial Decryption

## IND-CCA2  [concept_ind_cca2]  (property; 10 papers)
Adaptive chosen-ciphertext security makes shared secrets indistinguishable from random even when an attacker can request decapsulation of arbitrary other ciphertexts; it corresponds to active-attack security and supports key reuse.
Papers: 2010_corrigangibbs_dissent, 2014_syta_dissentanalysis, 2016_hopwood_zcash_protocol_spec, 2017_kwon_atom, 2018_unger_deniable, 2019_stebila_rfc9954_hybridtls, 2024_nist_fips203, 2025_auerbach_cgka_no_pruning
- compares_with: Key Privacy
- provides: Ciphertext indistinguishability

## PyBitmessage  [concept_pybitmessage]  (system; 7 papers)
Signal's employed signature scheme is XEdDSA; the text says its signing and verification typically require the same computation as a Diffie-Hellman key computation in an asymmetric ratchet step.
Papers: 2012_bitmessage_wiki_changelog, 2012_bitmessage_wiki_faq, 2015_bip47_paymentcodes, 2016_kysek_minode_readme, 2018_bitmessage_wiki_main_rce_notice, 2022_dowling_continuous_authentication, 2026_luka0614_bitmessage_quantum_assessment
- attacks: Remote code execution vulnerability in PyBitmessage 0.6.2
- defends_against: Remote code execution vulnerability in PyBitmessage 0.6.2
- instance_of: Bitmessage
- provides: Anonymous bridge claim; Deanonymisation mitigation; Encrypted broadcasts; Inventory flooding mitigation; Network transfer rate limit; Trusted peer option
- requires: Maximum object size
- uses: AES-CBC; Bootstrap nodes; Connection timeout; Default PoW difficulty; Embedded-time fuzzing; I2P; Inventory relay; Inventory storage; Message storage database; Opportunistic TLS

## Addra  [concept_addra]  (system; 5 papers)
Closest related protocol; computational PIR provides privacy even if infrastructure and all users except communication partners are malicious, but it natively supports only one-to-one calls. Its evaluated parameters fail the stated mouth-to-ear recommendation.
Papers: 2021_ahmad_addra, 2022_zhang_formal_def_metadata_private_messaging, 2024_coijanovic_pirates, 2024_tovey_distributedpir, 2025_kaviani_myco
- assumes: Fully untrusted infrastructure; Single-server CPIR trust choice
- compares_with: Pirates
- contradicts: PIR scalability limit
- implements: Caller mailbox and two-hop delivery; Master-worker architecture; PIR query cost amortization
- improves_on: Yodel 20-percent server assumption
- leaks: Call choice leakage
- measures: AWS prototype evaluation; Ciphertext expansion; Client CPU per round; Client network per round; Latency at 32,768 users; Latency scaling; Mean jitter; Server CPU per subround
- proves: Relationship unobservability proof
- provides: Content privacy; Metadata Privacy; Relationship Unobservability
- requires: Continuous online client requirement; Subsecond latency target; Unlimited download condition
- uses: 128-bit mailbox authentication token; AES-CBC content encryption; Dialing protocol; FastPIR; LPCNet voice rate; Private Information Retrieval; Round and subround timing; Voice message encryption

## SimpleX  [concept_simplex]  (protocol; 10 papers)
The reviewed messaging system includes SMP, its agent protocol, push notifications, file transfer, XRCP, and chat protocols. Trail of Bits reviewed design documents and a simplified SMP queue-agreement model.
Papers: 2021_simplex_agent_protocol, 2021_simplex_smp_spec, 2022_simplex_chat_protocol, 2022_simplex_platform_overview, 2022_simplex_push_notifications, 2023_simplex_security_model, 2023_simplex_xrcp, 2024_trailofbits_simplex_design_review
- assumes: Global assumptions
- extends: Relay-mediated distribution
- implements: Two-router delivery path
- provides: Message formats; Network latency objective; Publish/Subscribe; SMP GET message-count side channel
- uses: Router buffering and expiration; SimpleX Messaging Protocol (SMP); TLS transport; XFTP file transfer

## Identity-Based Encryption (IBE)  [concept_identity_based_encryption]  (protocol; 10 papers)
IBE treats a username such as an email address as a public key, allowing encryption without a directory lookup. Alpenhorn uses it to encrypt first-contact requests and obtain recipient keys without revealing the recipient identity through a lookup.
Papers: 2004_boneh_peks, 2015_nholambe_maintenancetopology, 2016_lazar_alpenhorn, 2019_doku_zephyr, 2021_beck_fmd, 2023_rosler_upibe, 2024_coijanovic_pirates, 2024_mongardini_stealthbeyond
- hides: Metadata Privacy
- improves_on: Download all messages
- instance_of: Boneh–Franklin IBE
- provides: Ciphertext Anonymity
- requires: Certification Authority (CA); Key server

## AES counter mode  [concept_aes]  (primitive; 11 papers)
The cited RSS security scheme enhances AES with D-AES for security and interception-loss improvements; this chunk provides no parameters or measurements for AES.
Papers: 2004_borisov_otr, 2016_matrix_megolm_spec, 2017_kiss_psiunequal, 2018_giacon_kem_combiners, 2019_jaques_grover_aes, 2019_kales_contactdiscovery, 2019_malina_secure, 2021_quarkslab_session_audit
- defends_against: Harvest Now, Decrypt Later Attack; Unauthenticated attachment access
- measures: AES circuit cost estimates
- provides: Transcript forgeability
- uses: Shared ByteSub auxiliaries; [BP12] S-box implementation

## Data Distribution Service (DDS)  [concept_data_distribution_service]  (protocol; 4 papers)
DDS provides real-time, scalable, data-centric pub/sub and supports asynchronous, time-independent delivery, anonymous location decoupling, and efficient bandwidth use. Its discovery maintains local databases of active writers and readers within a domain.
Papers: 2015_hakiri_publishsubscribe, 2023_peeroo_survey, 2024_chovet_performancecomparison, 2026_choi_roswhen
- compares_with: AMQP; MQTT; OPC UA; RabbitMQ; TCP; ZeroMQ
- instance_of: Publish/Subscribe
- leaks: Topic discovery
- measures: DDS burst and wireless results; DDS throughput at 5 KB; DDS versus HLA; DDS versus socket latency; Default-QoS latency results; High-frequency DDS and MQTT throughput; Large-message implementation results; Latency size threshold; OpenSplice participant limit; OpenSplice small-message performance
- provides: Anonymous asynchronous many-to-many messaging; Bounded resources over intermittent links; Content-Based Pub/Sub; DDS batching mode; DDS fine-grained security permissions; DDS participant discovery database; DDS partition isolation; Message replay after reconnection; Multi-channel predicate filtering; Topic-Based Pub/Sub
- requires: DDS conversion overhead
- uses: Safe-mode message retention; Simple Endpoint Discovery Protocol (SEDP); Simple Participant Discovery Protocol (SPDP); UDP

## ZIPNet  [concept_zipnet]  (protocol; 1 papers)
Anonymous broadcast protocol using two DC nets in parallel, a schedule and a message channel. It targets low message sizes, few broadcasters per round, and many cover clients.
Papers: 2024_rosenberg_zipnet
- assumes: Aggregator trust scope; Anytrust Model; Global channel observer; Honest client fraction; Synchrony assumption; TEE security not assumed
- compares_with: OrgAn speedup; Riposte; TEE alternatives; ZIPNet Blinder server speedup
- defends_against: Schedule equivocation attack; Trusted Execution Environment (TEE)
- extends: DC-net; Subset server participation; Threshold failover
- implements: Two-network round sequencing
- improves_on: Compression costs; Dissent
- instance_of: Anonymous Broadcast Channel; DC-net
- measures: Aggregator linear message cost; Client runtime benchmarks; Server count runtime effect; Server cover bandwidth cost; Server instance cost; Server runtime gain; Talking-client quadratic server cost; WAN network conditions
- motivates: Anonymity Trilemma; Trust diversity rationale
- provides: Broadcast anonymity; Client and server message sizes; Client message malleability; Cover bandwidth cost; Forward Secrecy; Hundreds of servers; Server computation offload; ZIPNet overall speedup
- requires: Anytrust anonymity condition; Anytrust server failure abort; Minimum participation threshold; Offline reservation restart
- uses: AES-NI server acceleration; Aggregation outsourcing; Attestation setup amortization; Client per-server OTP work; Cover Traffic; Cover traffic clients; Fixed round configuration; Footprint Scheduling; Schedule shared context; Scheduling parameters

## Kopis  [concept_kopis]  (protocol; 1 papers)
A KEM with constant-time algorithms, 32-byte seed secret keys, TurboSHAKE-based operations, and formal Rust verification. The chunk benchmarks it against ML-KEM and Saber and evaluates it in PAKE and OKEX estimates.
Papers: 2026_basso_kopis
- assumes: Random oracle simulation
- compares_with: ML-KEM; Saber
- extends: Saber
- improves_on: Cortex-M4 hashing fraction; ML-KEM
- measures: AVX2 KEM runtimes; Benchmark comparison; Ciphertext size comparison; Classical security estimates; Cortex-M4 KEM runtimes; Cortex-M4 memory use; Decryption failure probabilities; KEM key and ciphertext sizes; Kopis-512 packet fit; Portable KEM runtimes
- proves: CRq collision bound; IND-CCA; Rust implementation verification
- provides: ANO-PCA; CRq; Ciphertext Second Preimage Resistance; Constant-time algorithms; Constant-time implementation; IND-CCA KEM; Kopis key-exchange payload; Kopis secret key size; Kopis-512 UDP packet fit; MAL-BIND-K-CT
- requires: Binomial parameter μ; Compression parameter t; Public matrix dimension; Secret key
- uses: Constant-time validation; Fujisaki–Okamoto transform; IND-CPA PKE; Kopis parameter sets; Matrix generation; Module Learning With Rounding; Polynomial ring parameters; Secret generation; TurboSHAKE

## Digital signatures  [concept_digital_signature]  (primitive; 11 papers)
A digital signature has key generation, signing and verification algorithms. Strong correctness requires each message-signature pair to verify for every signing randomness; the paper uses signature strong correctness in its eSM correctness bound.
Papers: 2004_borisov_otr, 2018_durak_linear_ratcheting, 2020_dias_mqttmecanismo, 2021_hashimoto_pq_x3dh_deniable, 2022_cremers_pq_secure_messaging, 2023_balbas_sender_keys, 2023_bicer_ohe, 2024_argo_pq_signatures_privacy
- compares_with: Ring signature
- contradicts: Repudiability
- leaks: Minimal disclosure claim
- provides: Authentication, integrity, and non-repudiation; SUF-CMA security

## Delay-Tolerant Network  [concept_delay_tolerant_network]  (concept; 11 papers)
The target network environment has intermittent delivery challenges; network-coding broadcast can cause redundancy, invalid transmissions, and congestion. The paper evaluates its method in a simulated DTN.
Papers: 2011_guidec_communicationbasee, 2011_nguyen_swarmintelligent, 2012_ciobanu_data, 2013_royer_survey, 2015_barroso_adtn, 2015_royer_performancecontext, 2016_briar_bsp, 2016_lerner_rangzen
- uses: Store Carry and Forward; Temporal path

## secp256k1  [concept_secp256k1]  (primitive; 10 papers)
The elliptic curve used for Bitcoin keys and Tithonus registration; the chunk describes encoding encrypted data into candidate x-coordinates for this curve.
Papers: 2012_bitmessage_wiki_changelog, 2018_recabarren_tithonus, 2021_tron_book_of_swarm, 2021_vac_waku2_payload_spec, 2022_erc5564_stealth, 2022_vac_waku2_x3dh_spec, 2023_bip352_silent_payments, 2023_wahrstatter_basesap
- uses: ECDH

## Ring learning with errors  [concept_ring_learning_with_errors]  (primitive; 10 papers)
YPIR uses RLWE for response packing, and its preprocessing optimization changes the security basis from LWE to RLWE. The chunk defines the normal-form assumption as computational indistinguishability of (a,sa+e) and uniform (a,v).
Papers: 2015_ghosh_pq_onion, 2017_polyakov_fast, 2022_lin_deprir, 2023_abdennebi_latticepubsub, 2023_liu_gomr, 2023_patel_keywordpirsparse, 2024_lee_sophomr, 2024_liu_perfomr

## Private Set Intersection (PSI) protocol  [concept_private_set_intersection]  (protocol; 5 papers)
PSI lets a client obtain the intersection of client set C and server set S without learning additional elements of S, while the server learns no information about C. Batch keyword PIR can supply the intersection but needs additional techniques for server privacy.
Papers: 2017_chen_psihe, 2018_demmler_pirpsi, 2021_hagen_contact_discovery, 2022_hagen_contactdiscovery, 2026_arunachalaramanan_pirsurvey
- assumes: Semi-honest security
- contradicts: Enumeration attack; PSI does not prevent enumeration
- extends: Larger-receiver-set variant
- measures: Asymmetric-set communication; Low-bandwidth runtime; PSI transfer at 2^28 users; PSI transfer at 2^31 users; Receiver computation
- proves: Communication complexity
- provides: PSI does not prevent enumeration
- requires: Circuit privacy; Per-instance hash-function use
- uses: Batching; Fully homomorphic encryption (FHE); Hashing for indexing; Modulus switching; Partitioning; Private Information Retrieval; Windowing

## XRD (Crossroads)  [concept_xrd]  (system; 6 papers)
A multiple-cascade design whose cascade-selection scheme guarantees every pair of users shares at least one cascade; its described client dummy scheme sends Nc−1 dummies per real message and routes each message on a different chain, at high bandwidth cost.
Papers: 2020_kwon_xrd, 2021_benguirat_mixim, 2021_das_divide_and_funnel, 2021_eskandarian_express, 2023_sasy_sokmetadata, 2026_eldefrawy_pib3
- assumes: Adversary model; Cryptographic assumptions; Online user assumption
- compares_with: Alpenhorn; Atom; DP family; Karaoke; Private Information Retrieval; Pung; Relative performance; Stadium
- defends_against: Cascade Partitioning
- improves_on: Atom
- instance_of: CUS; Mixnet
- measures: Latency evaluation; User bandwidth estimate; XRD Message Cost
- provides: Cryptographic metadata privacy; Server workload scaling
- requires: Anytrust mix chains; Out-of-band conversation start
- uses: Aggregate hybrid shuffle; Authenticated encryption; Client Dummy Cost; Key Transparency; Loopback messages; Mixnet; Next-round cover messages; Onion encryption for chains; Public chain intersection; Public mailbox association

## Universal composability (UC) framework  [concept_universal_composability]  (concept; 9 papers)
The paper formalizes security by requiring real-world execution to be indistinguishable from an ideal-world functionality to an interactive environment; it uses responsive environments to avoid modeling local operations as involving the adversary.
Papers: 2005_camenisch_onion_formal, 2018_unger_deniable, 2020_alwen_mls_insider, 2021_alwen_server_aided_cgka, 2021_madathil_privatesignaling, 2024_hansen_ocash, 2024_klooss_eror, 2024_rial_outfox
- assumes: Adversary network control; Continuous state leakage corruption model
- implements: Temporary identifier ideal functionality
- provides: UC security theorem
- requires: Restricted admissible environments
- uses: Ideal functionality

## Authenticated encryption with associated data  [concept_aead]  (primitive; 10 papers)
PQXDH and X3DH encrypt the initiator’s first user message with AEAD under the derived session key. Signal’s implementations derive the nonce deterministically from the key, so the paper omits it in notation.
Papers: 2021_duguey_thesis, 2023_beguinet_tamarin_pqsignal, 2024_bhargavan_pqxdh, 2024_collins_dr_tight, 2024_fiedler_pqxdh_deniability, 2024_rial_outfox, 2025_albrecht_whatsapp_multidevice, 2025_auerbach_pq_metric
- requires: Classical computational security theorem
- uses: Encrypt-then-MAC; Hybrid Public Key Encryption

## CoCoA  [concept_cocoa]  (mechanism; 6 papers)
CoCoA accepts as many concurrent update proposals as possible but rejects one update where two updates conflict at a node. It heals after each compromised party updates log(n) times in the worst case; recipient download is at most log(n) ciphertexts per concurrent set, independent of m and t, with a sophisticated server.
Papers: 2018_anon_publishsubscribe, 2022_alwen_cocoa, 2022_alwen_decaf, 2023_auerbach_pcs_cost_concurrent, 2025_auerbach_cgka_no_pruning, 2025_lebrun_thesis
- compares_with: Adaptive RTO; BDR20 communication lower bound; Insider security; Post-Compromise Security; TreeKEM
- implements: Concurrent add operations; Concurrent remove operations; Server-aided CGKA; Winner selection on conflicting rotations
- instance_of: Continuous Group Key Agreement (CGKA)
- proves: Adaptive partially active adversary; Arbitrary server winner recovery
- provides: CoCoA concurrent communication; CoCoA update rounds; Partial update recovery; Post-Compromise Security; Weak robustness
- requires: Signature key communication
- uses: Component signatures; Concurrent update ordering; Lite updates; Parent hash; Partial tree state; Round hash; TreeKEM

## Swarm PSS  [concept_swarm_pss]  (protocol; 4 papers)
Postal Service on Swarm provides direct node-to-node messaging by encrypting for the recipient and wrapping the message with a topic in a content-addressed chunk placed in the recipient’s neighborhood. It supports asynchronous delivery and topic dispatch after decryption.
Papers: 2018_ethersphere_pss_readme, 2021_tron_book_of_swarm, 2021_tron_swarm_whitepaper, 2026_urushigaki_session_attacks
- assumes: Development status
- implements: Decrypting peers forward messages; Recipient neighborhood delivery; Topic-Based Pub/Sub
- instance_of: Publish/Subscribe
- motivates: Feed topic-index addressing
- provides: Asymmetric send; Asynchronous persistent delivery; Duplicate message delivery; No delivery guarantee; Optional Diffie-Hellman handshake; PSS topic messaging API; Postage-controlled mailbox; Publish/Subscribe; Random target success probability; Symmetric send
- requires: Deterministic initial Swarm assignment; Kademlia; PSS message requirements; Per-topic peer key registration; Recipient decryption work
- uses: Content-Addressed Chunk; Partial-address routing; Recipient decryption and topic check; Swarm; Trojan chunk format; Trojan chunks; Whisper; X3DH

## Session  [concept_session]  (system; 7 papers)
The analyzed Legacy Groups protocol has exploitable insider replay and outsider ciphertext replay attacks. Outsiders can modify the unauthenticated timestamp used for replay detection; a compromised member signing key also permits outsider forgery because public keys are used as group identifiers.
Papers: 2020_jefferys_session, 2021_quarkslab_session_audit, 2025_jaeger_group_chat_encryption, 2025_session_protocol_v2, 2026_esposito_verbeth, 2026_firmansyah_decentralized_messaging_metadata, 2026_urushigaki_session_attacks
- assumes: Audit threat models
- attacks: Insider replay attacks; Session outsider replay; Session signing key exposure forgery
- compares_with: BitChat; Ethereum
- implements: Session Legacy Groups
- instance_of: Sign then Encrypt; Symmetric signcryption
- provides: Metadata Privacy; Session attachment metadata; Session onion hop logs; Session recovered metadata records
- uses: Libsodium; Long-Term Key (LTK); Onion Routing; Oxen network; Pseudonymous key-based identity; SQLCipher; Session Protocol V1; Staked Session Node network

## Replay attack  [concept_replay_attack]  (attack; 10 papers)
An attacker replays observed authentication messages to impersonate a trusted party. The proposed protocol claims protection by checking G, the publisher public and private keys, and the topic ID.
Papers: 2009_danezis_sphinx, 2013_tor_prop224_rendng, 2016_galteland_cmixattacks, 2016_matrix_megolm_spec, 2017_chaum_cmix, 2018_shirazi_survey_routing_anon, 2019_malina_secure, 2020_weidner_decentralized_sgm
- defends_against: Authenticated channels; Signature and timestamp sizes
- instance_of: Message replay limitation

## BBS signature scheme  [concept_bbs_signature_scheme]  (primitive; 5 papers)
A multi-message signature scheme that produces one constant-size signature and supports zero-knowledge proofs that selectively disclose signed messages while preserving their authenticity and integrity.
Papers: 2015_unger_sok_securemessaging, 2023_agrawal_traceablemixnets, 2025_draft_bbs, 2025_slamanig_privacy_auth, 2026_draft_act
- assumes: n-Strong Diffie–Hellman assumption
- instance_of: BBS+ signatures
- provides: Constant-size signature; Proof length floor; Proof of possession; Proof value unlinkability; Selective disclosure
- requires: Message order requirement; Unique pseudo-random generators
- uses: API domain separation; Fiat-Shamir challenge; Pairing verification; Pedersen commitment; Proof challenge check; Validate signature before proving; Zero-Knowledge Proof

## BASALT  [concept_basalt]  (protocol; 2 papers)
BASALT is a Byzantine-tolerant random peer sampling algorithm that uses stubborn chaotic search and min-wise independent permutations; its view is managed by the sampler. It is intended for large networks and sampling-based consensus such as Avalanche.
Papers: 2023_auvolat_basalt, 2026_mukam_byzantineresilient
- assumes: Attack force; Byzantine nodes; Complete communication network assumption
- defends_against: Eclipse Attack
- extends: Brahms
- improves_on: Brahms; Proof of Stake; SPS; Tolerance-based defenses
- instance_of: Peer Sampling
- measures: Basalt evaluation; Live cryptocurrency deployment; Monte Carlo evaluation
- proves: Byzantine sample probability; Correct identifier discovery bound; Isolation probability bound; Stable equilibrium B1
- provides: Epidemic BFT sampling motivation; Sampling rate ρ
- requires: Exchange interval τ; Sybil resistance resource requirement; View size v
- uses: Basalt seed refresh; Gossip protocols; Hash-function minimization; Replacement count k; Stubborn chaotic search

## Vitis  [concept_vitis]  (protocol; 9 papers)
A gossip-based hybrid, topic-based P2P publish/subscribe overlay for Internet-scale use. It uses bounded node degree, subscription-similarity neighbor selection, rendezvous routing, gateways, relay paths, and small-world links.
Papers: 2011_mega_dissemination_decentralized, 2012_rahimian_locality_awareness, 2012_setty_poldercast, 2013_mega_social_overlays, 2014_chen_overlay_network, 2018_chen_beaconvey, 2019_vyzovitis_gossipsub_v01, 2020_savolainen_streamr_network
- compares_with: Millions-node scale target; PolderCast
- contradicts: Topic-Connected Overlay
- extends: Small-world fingers
- implements: Notification and event pull
- improves_on: Scribe
- instance_of: Publish/Subscribe; Topic-Based Pub/Sub; Topic-Connected Overlay
- requires: Bounded degree and relay trade-off
- uses: Peer Sampling; Rendezvous Point; Topic cluster

## CONIKS  [concept_coniks]  (protocol; 8 papers)
An academic public-key-directory transparency design that formalized a service maintaining and periodically committing to a directory. It uses synchronous gossip among users to detect server equivocation, which the excerpt says is hard to scale to millions and breakable over the internet.
Papers: 2015_unger_sok_securemessaging_tr, 2017_halpin_nextleap, 2018_chase_seemless, 2021_hu_merkle2, 2022_tzialla_transparencydictionaries, 2023_malvai_parakeet, 2024_brorsson_consistency_or_die, 2024_len_elektra
- compares_with: Append and lookup tradeoff
- improves_on: SEEMless comparison
- leaks: Key-update timing exposure
- measures: CONIKS heap limit; CONIKS history monitoring cost; CONIKS monitoring cost; CONIKS self-auditing bandwidth cost; Epoch-by-epoch history cost
- provides: Proof of absence
- uses: Hash chain; Merkle key-presence verification; Prefix tree; Synchronous user gossip

## Ring-LWE  [concept_ring_lwe]  (assumption; 8 papers)
The encryption scheme provides indistinguishability against chosen-plaintext attacks if the standard lattice problem Ring-LWE is hard. The paper characterizes Ring-LWE as a standard and widely used lattice assumption.
Papers: 2016_aguilarmelchor_xpir, 2021_liu_omr, 2022_henzinger_simplepir, 2022_lin_deprir, 2023_beullens_lattice_blind_sig, 2023_lai_commit_transferrable_sig, 2024_liu_snakeeye, 2025_mikic_pqstealth
- assumes: Worst-case lattice hardness basis
- attacks: Ring-LWE coefficient correlation attack; Snake-eye attack
- instance_of: Module lattice assumptions
- provides: Chosen-plaintext indistinguishability
- uses: NewHope

## Quantum random oracle model  [concept_quantum_random_oracle_model]  (protocol; 8 papers)
The model grants adversaries quantum access to idealized, unkeyed random-oracle primitives, while oracles modeling honest parties and taking inputs unknown to the adversary receive conventional queries. The paper states its SPHINCS+ instance has a tight QROM proof.
Papers: 2017_bindel_transition_pki, 2017_bos_kyber, 2018_bindel_hybrid_kem_ake, 2019_bernstein_sphincsplus, 2022_grubbs_anonrobustpq, 2022_maram_pq_anonymity_kyber, 2022_park_superlinearity, 2022_xagawa_anonymitykems
- provides: Quantum Random Oracle Collision Bound; Quantum Random Oracle PRF Bound; Quantum adversary
- uses: EUF-CMA

## ECDSA  [concept_ecdsa]  (primitive; 9 papers)
Conventional certificate signature based on elliptic-curve discrete-log hardness; the study uses secp384r1 (192-bit classical security) as a baseline, while describing its post-quantum security as approximately zero bits.
Papers: 2017_pybitmessage_repo_protocol_docs, 2018_marcus_ethereumeclipse, 2020_sikeridis_pq_tls_performance, 2020_yu_stealthschemes, 2021_vac_waku2_payload_spec, 2022_vac_waku2_x3dh_spec, 2024_juaristi_pq_ethereum, 2025_slamanig_privacy_auth
- compares_with: ComSig
- provides: EUF-CMA
- uses: Keccak-256; Semi-injective conversion function; secp256k1

## Spectrum  [concept_spectrum]  (system; 4 papers)
Spectrum provides blind access control and a Blame-Game protocol against malicious servers rejecting valid writes. It permits server-writer collusion under discrete-log hardness, but visible verification-key updates prevent oblivious authorization updates.
Papers: 2022_newman_spectrum, 2023_sasy_sokmetadata, 2026_li_pepper, 2026_ravi_remise
- assumes: Client adversary model; Cryptographic assumptions; Network observer
- compares_with: Blinder; Client denial of service; Dissent; Express; Pepper; Riposte
- defends_against: Selective deanonymization attack
- measures: 1 GB deployment result; Throughput comparison
- motivates: Messaging V1
- provides: Availability conditions; Bandwidth scaling; Per-request server work; Public broadcast output
- requires: Anonymous key bootstrap; Cover traffic requirement; Online duration; Server trust assumption
- uses: Anonymous access control; BlameGame; Client-server transport encryption; DC-net; Distributed Point Function; Multi-server DPF key size; Two-server DPF key size

## RSA  [concept_rsa]  (primitive; 8 papers)
The RSA trapdoor permutation is not anonymous: ciphertext values can reveal which of two moduli was used even when moduli have the same length. The paper assumes RSA one-wayness for its proposed anonymous variants.
Papers: 2001_bellare_keyprivacy, 2009_danezis_sphinx, 2012_mulamba_design, 2015_decouchant_collusions, 2015_heimgaertner_security, 2017_bindel_transition_pki, 2020_sikeridis_pq_tls_performance, 2026_mallick_aquaman
- attacks: RSA modulus comparison attack
- implements: Encrypted signing-key embedding

## DDS  [concept_dds]  (system; 6 papers)
OpenDDS is configured with RTPS discovery and unicast transport in the cluster; default TCP ensures messages traverse network cards even on the single-node testbed. High QoS uses reliable delivery, transient durability depth 5, and a one-second liveliness lease.
Papers: 2011_sanchezmonedero_ddsbloom, 2022_junior_performancepublish, 2023_corsaro_zenohunifying, 2023_liang_zenohperformance, 2024_mehran_runtimeverification, 2026_badolato_psmarkdistributed2
- compares_with: DDS bandwidth versus MQTT
- instance_of: Topic-Based Pub/Sub
- leaks: Broker can read unencrypted payload; DDS discovery bottleneck
- provides: Packet size ordering; Publish/Subscribe
- uses: DDS-RTPS; Topic-Based Pub/Sub

## Cyclon  [concept_cyclon]  (protocol; 8 papers)
A decentralized peer-sampling protocol in which each node maintains a partial view and periodically swaps descriptors with a neighbor. Its view length ℓ is typically 20–50; churn and random mixing support scalable, self-healing overlays.
Papers: 2012_matos_brisa_combining, 2012_setty_poldercast, 2013_rene_erreichen, 2019_wael_improve, 2020_savolainen_streamr_network, 2022_zaarour_openpubsub_supporting, 2026_mukam_byzantineresilient, iog_securecyclon_dependable_peer_sampling
- assumes: Descriptor size and growth
- compares_with: Cyclon and Vicinity shortcut mix
- instance_of: Default view size 20; Peer Sampling
- motivates: Random peer sampling
- provides: Cyclon view size; Indegree equilibrium
- uses: Partial view and periodic exchange; Tit-for-tat descriptor transfer

## Collision Resistance  [concept_collision_resistance]  (property; 8 papers)
Several specified hash functions and PRFs have collision-resistance requirements. Sapling and Orchard Merkle hashes must be collision-resistant on all arguments, while the Sprout Merkle hash is excepted on its first argument.
Papers: 2014_syta_dissentanalysis, 2016_hopwood_zcash_protocol_spec, 2019_bernstein_sphincsplus, 2020_schwabe_kemtls, 2022_tzialla_transparencydictionaries, 2024_jaeger_keybase_signcryption, 2025_hashimoto_bundled_ake, 2025_wallez_treekem_verified
- proves: sm-tcr
- requires: GroupInfo

## PriFi  [concept_prifi]  (protocol; 3 papers)
PriFi is cited as a recent DCN implementation among exceptions to the survey's statement that legacy methods are inappropriate for latency-sensitive applications. The table describes it as a three-layer low-latency architecture that keeps packets on the usual local low-latency path and is deployable with minimal infrastructure changes.
Papers: 2017_barman_prifi, 2019_lu_survey, 2022_shirali_dcnetsurvey
- assumes: Anytrust guard assumption; Closed membership; Malicious but available relay; PriFi any-trust guards
- compares_with: Dissent in Numbers latency 14.5 seconds; Intersection attack; Legacy DCN Latency Limits; Mixnet; Onion Routing; Tor path-compromise attack metric
- contradicts: PriFi intersection attack limitation
- defends_against: Disruption attack; Equivocation attack; Traffic Analysis
- implements: Client-relay-guard architecture
- improves_on: Dissent
- leaks: Aggregate traffic feature leakage; Relay sees upstream plaintext
- measures: About 100 ms overhead at 100 clients; About 40 Mbps in 100 Mbps LAN; ICRC trace latency increase
- proves: Two orders lower latency
- provides: Negligible attribution advantage; PriFi equivocation defense
- requires: At least two honest clients; PriFi minimum honest clients
- uses: DC-net; Downstream UDP broadcast; Equal-length upstream ciphertexts; History-bound encryption; Load tuning; Lock-step schedule slots; PriFi epoch; Retroactive hash-based blame; Verifiable shuffle setup

## Pseudorandom generator  [concept_pseudorandom_generator]  (primitive; 8 papers)
In the Sender Key Mechanism, each send refreshes the chain key and outputs a message key. Receivers advance the chain to the indicated counter to tolerate out-of-order delivery.
Papers: 2019_corrigangibbs_sublinear_pir, 2021_beck_fmd, 2022_canetti_uc_messaging, 2023_eskandarian_abusereporting, 2023_rosler_upibe, 2025_collins_gurke, 2025_gunther_hybrid_obfuscated_kex, iog_modular_design_of_secure_group_messaging_protocols_and_the_s
- provides: PRG-to-set security composition

## SHA-512  [concept_sha_512]  (primitive; 7 papers)
SHA-512 is the on-wire MLS derivation hash for path secrets and the key schedule; it is modeled independently from Poseidon2. Grover reduces preimage security to 192 bits at λ=384 and 256 bits at derivation width 512.
Papers: 2015_maloney_dpush, 2016_boneh_balloon, 2016_hopwood_zcash_protocol_spec, 2017_pybitmessage_repo_protocol_docs, 2024_jaeger_keybase_signcryption, 2024_nist_fips205, 2026_mangipudi_auditable_cgka
- implements: Balloon Hashing; MLS
- measures: Compression function throughput result

## Ricochet  [concept_ricochet]  (protocol; 7 papers)
Ricochet, first released in 2014, used Tor v2 onion services for end-to-end encrypted communication and metadata protection, with no centralized routing servers. Only conversation parties could know a conversation was taking place, but it lacked multi-device, group, and offline messaging support.
Papers: 2015_unger_sok_securemessaging, 2015_unger_sok_securemessaging_tr, 2016_ncc_ricochet_audit, 2018_lewis_cwtch, 2021_cwtch_risk_model, 2021_cwtch_security_handbook, 2022_ricochet_refresh_design
- assumes: State-level adversary
- provides: Anonymity properties; Censorship and monitoring resistance; Forward Secrecy; Privacy and security goals
- requires: Ricochet limitations
- uses: Binary command/reply protocol; Hidden Services; Tor

## cMix  [concept_cmix]  (protocol; 3 papers)
A fixed cascade mixnet protocol using precomputation to eliminate real-time public-key operations in its core protocol. Its anonymity theorem assumes CPA-secure group-homomorphic encryption, perfectly hiding non-interactive commitments, protocol integrity, and the random oracle model.
Papers: 2016_galteland_cmixattacks, 2017_chaum_cmix, 2021_benguirat_mixim
- assumes: Corruption limits; Decision Diffie–Hellman assumption; Network handler
- compares_with: Onion Routing
- hides: Batch relationship visibility
- instance_of: Mix networks; Mixnet
- measures: Operation-count comparison
- part_of: Privategrity
- provides: Linear scaling; Low real-time cryptographic latency; Real-time public-key operation elimination; Replay protection
- requires: Batch parameters; Batch size β; Message-length limit; Mix node count n
- uses: Cascade; Fixed cascade; Mixnode-only precomputation; Multiparty group-homomorphic ElGamal; Network handler; Offline precomputation phase; Per-node sender keys; Real-time phase

## HMAC  [concept_hmac]  (primitive; 7 papers)
HMAC is presented as a suitable choice for CEP's collision-resistant PRF, with formal support for PRF security under a secret key and collision resistance for adversarially chosen same-length keys assuming the hash function is collision resistant.
Papers: 2016_matrix_megolm_spec, 2017_grubbs_franking, 2018_davidson_privacypass, 2020_schwabe_kemtls, 2021_duguey_thesis, 2023_albrecht_matrix, 2024_nist_fips205
- defends_against: No malicious acceptance under assumptions
- instance_of: Message authentication code (MAC)
- provides: 64-bit MAC truncation; Multi-instance strong unforgeability

## KEMTLS  [concept_kemtls]  (protocol; 1 papers)
TLS 1.3 alternative using KEMs for ephemeral key exchange and server authentication. It aims to preserve the same round trips to the client's first encrypted application data while reducing communication and computation.
Papers: 2020_schwabe_kemtls
- assumes: Root CA trust-store assumption
- compares_with: OPTLS; TLS 1.3
- contradicts: Online deniability absent; Server anonymity limitation
- extends: TLS 1.3
- implements: Three handshake phases
- improves_on: Handshake size reduction
- measures: Lattice variant speedup; Round 3 handshake size comparison; SIKE size variant slowdown; Server CPU reduction
- proves: Match security; Theorem 4.1 advantage bound
- provides: Client first application data; Client stage-key properties; Downgrade resilience; Explicit authentication; Implicit authentication; Less than half bandwidth; Offline certificate signing; Offline deniability; Post-quantum authentication; Same round trips to first data
- requires: Client verification code; IND-CCA
- uses: HKDF; Key Encapsulation Mechanism; Multi-stage AKE model; Signature scheme (Sig)

## Authenticated Encryption with Associated Data  [concept_authenticated_encryption_with_associated_data]  (primitive; 8 papers)
AEAD encrypts a message with associated data and returns ciphertext and tag; decryption returns the message or failure. The chunk defines IND-CCA security with test pairs and encryption/decryption oracles, excluding decryption queries matching the challenge ciphertext or tag.
Papers: 2022_barnes_rfc9180, 2022_bienstock_dr_uc, 2022_cong_key_lattice, 2023_bienstock_asmesh, 2024_bhargavan_pqxdh, 2024_fiedler_pqxdh_deniability, 2025_dodis_triple_ratchet, iog_modular_design_of_secure_group_messaging_protocols_and_the_s
- requires: AEAD ciphertext explainability; One-time IND-CCA security

## NIZK  [concept_nizk]  (primitive; 8 papers)
The NIZK interface has Setup, Prove, Verify, and SimSetup, and requires completeness, soundness, and zero-knowledge. The chunk states Fiat-Shamir proofs satisfy these properties in the random oracle model, citing prior work.
Papers: 2014_bensasson_zerocash, 2017_kwon_atom, 2023_lai_commit_transferrable_sig, 2024_collins_k_waay, 2024_diaz_reliability, 2026_jarecki_x3dh_sas, iog_kachina_foundations_of_private_smart_contracts, iog_ouroboros_crypsinous_privacy_preserving_proof_of_stake
- compares_with: NIZK versus trap tradeoff; zk-SNARK
- defends_against: Malicious sender acceptance condition
- implements: Private stake eligibility proof
- provides: Mixnet
- uses: Fiat-Shamir

## Herd  [concept_herd]  (system; 2 papers)
A low-delay anonymity network for VoIP that combines trusted, fully connected mixes with optional untrusted superpeers. It provides caller and callee zone anonymity under a global passive and local active traffic-analysis threat model.
Papers: 2015_leblond_herd, 2020_lazar_thesis
- assumes: Global passive, local active adversary; PKI root of trust; Rational SP behavior; Trust in attached mix
- compares_with: Aqua; Dissent; Drac
- measures: Client link bandwidth cost; Evaluation trace scale; Prototype latency result
- provides: Herd comparison; Zone anonymity
- uses: Constant-rate padding; Dynamic chaffing; Fully connected mix network; Hop-by-hop encryption; Hybrid architecture; Layered encryption; Network coding; Rendezvous mechanism; Trust zone

## Collision-resistant hash function  [concept_collision_resistant_hash_function]  (primitive; 8 papers)
A hash function used by the KT scheme and Patricia trie. Its security condition bounds the probability of finding distinct inputs with the same hash by a negligible function of the security parameter.
Papers: 2001_bellare_keyprivacy, 2018_bhargavan_treekem, 2018_chase_seemless, 2018_durak_linear_ratcheting, 2020_jacob_matrix_event_graph, 2021_ando_cryptographic_shallots, 2023_len_optiks, 2024_brandt_kt_sok
- provides: Reference Monitor

## Intel Software Guard Extensions (SGX)  [concept_sgx]  (primitive; 6 papers)
Hardware trusted execution environment isolating application code and data in enclaves from applications and privileged software. Enclave memory is encrypted by the CPU’s Memory Encryption Engine and hardware access controls prevent snooping or tampering; the CPU package is assumed uncompromised.
Papers: 2016_pires_secure, 2017_havet_securestreams, 2017_kim_sgxtor, 2018_arnautov_pubsubsgx, 2018_wust_zlite, 2021_pasdar_oracle_design_patterns

## Triple Ratchet  [concept_triple_ratchet]  (protocol; 4 papers)
A hybrid protocol that runs a Double Ratchet and SPQR in parallel, combines their 32-byte message keys with a KDF, and uses the result as the encryption key. The chunk reports a proof of hybrid security: breaking both elliptic-curve and post-quantum assumptions is required.
Papers: 2016_signal_double_ratchet_spec, 2022_bienstock_dr_uc, 2025_dodis_triple_ratchet, 2026_chu_anamorphic
- assumes: Random oracle model
- defends_against: Harvest Now, Decrypt Later Attack; Short-interval multiple-compromise weakness
- extends: CKA; Double Ratchet
- implements: Deterministic exponent update; HKDF
- improves_on: Double Ratchet; UPKE communication saving; rTreeKEM communication saving
- measures: One extra computation per epoch; Triple Ratchet collision bound
- proves: Correctness results; Double Ratchet; FTR functionality
- provides: Forward Secrecy; One group element communication; Post-Compromise Security; Triple Ratchet bandwidth; UPKE communication reduction
- uses: Continuous Key Agreement (CKA); Data chunking; Double Ratchet; Key derivation function (KDF); ML-KEM; Opportunistic sending; Sparse Post-Quantum Ratchet (SPQR)

## IND-CPA security  [concept_ind_cpa_security]  (property; 7 papers)
The FHE scheme is claimed to prevent an adversary given a public key and challenge ciphertext from guessing the selected message bit with probability greater than 1/2 plus negligible ε(λ).
Papers: 2017_chen_psihe, 2017_polyakov_fast, 2018_durak_linear_ratcheting, 2021_tian_iot_pubsub_access_control, 2022_maram_pq_anonymity_kyber, 2024_liu_snakeeye, 2025_hqc_specification
- proves: FHE Message Privacy Claim; IND-CCA2 advantage bound

## Oblivious RAM  [concept_oblivious_ram]  (primitive; 8 papers)
ORAM hides which entry is accessed in a client's private outsourced database. It can achieve amortized polylogarithmic communication and server computation in N with small constants; PIR addresses a public database, and comparable PIR complexity remains open.
Papers: 2017_marlinspike_signal_private_contact_discovery, 2018_wust_zlite, 2022_lin_deprir, 2023_jakkamsetti_scalablesignaling, 2024_jia_homerun, 2025_jiang_pingpong, 2025_kaviani_myco, 2026_arunachalaramanan_pirsurvey
- compares_with: Private Information Retrieval
- defends_against: Enclave memory access leakage
- hides: Recipient identity privacy; Signal count hiding
- leaks: ORAM timing leakage
- provides: ORAM same-length privacy condition

## Non-interactive zero-knowledge argument  [concept_non_interactive_zero_knowledge_proof]  (primitive; 7 papers)
The paper describes non-interactive ZKPs as allowing proof verification without interaction between prover and verifier, making them suitable for decentralized IIoT. Its workflow says the proof confirms access without revealing data D or public key PK.
Papers: 2021_hashimoto_pq_x3dh_deniable, 2023_bicer_ohe, 2023_liu_gomr, 2024_brandt_kt_sok, 2025_li_dpsiiot, 2026_zarchy_selfmix, iog_continuous_group_key_agreement_with_active_security
- provides: No trusted third party required

## Traceable mixnets  [concept_traceable_mixnets]  (protocol; 1 papers)
A threshold re-encryption mixnet lets senders encrypt sensitive values, shuffles and decrypts them, and supports BTraceIn/BTraceOut queries through distributed batched proofs. Secrecy is proved in the HBC setting; malicious-security steps are outlined.
Papers: 2023_agrawal_traceablemixnets
- assumes: Trusted dealer key setup
- compares_with: Distributed setting versus trusted curator
- defends_against: Intermediate linkage leakage
- extends: Mixnet
- hides: Query output visibility
- measures: Authenticated broadcast assessment; Benchmark setup; DB-RSM benchmark timings; DB-SM benchmark timings; Query proof data sizes; Sender proof cost
- proves: Completeness; Secrecy indistinguishability; Soundness
- provides: HBC secrecy theorem; Honest querier result hiding from servers; Linear batch time; Parallelism and recovery estimate; Query output leakage analysis; Query-output privacy; TraceIn query; TraceOut query; ΠTM output secrecy
- requires: Authenticated broadcast channel
- uses: BN254 curve; DB-RSM; DB-SM; Distributed mix-server provers; Fiat-Shamir heuristic; Pedersen commitment; Secret permutation composition; Sigma protocol; Threshold ElGamal encryption; Threshold Paillier encryption

## Pudding  [concept_pudding]  (protocol; 1 papers)
An application-layer private user discovery protocol that lets users be contacted on an anonymity network using an email address. It hides contact relationships, conceals username membership, prevents impersonation, tolerates up to one-third faulty discovery nodes, and was prototyped over Nym.
Papers: 2023_kocaogullar_pudding
- assumes: Discovery node fault assumption; Email service compromise; Email traffic observation
- defends_against: Pseudonymous registration membership test
- implements: Nym
- leaks: Provider message-count leak
- measures: Anonymous contact latency; End-to-end discovery latency; Lookup latency; Non-anonymous contact latency; Registration latency
- provides: Contact relationship hiding; External identity verification; Impersonation resistance; Lookup membership indistinguishability; Membership unobservability; Mobile and intermittent connectivity; One-party registration suffices; Unlinkability
- requires: Contact initiation retry limit; IND-CPA security; Key-blinded signatures; Lookup acceptance threshold; Registration challenge quorum; Registration confirmation quorum
- uses: Authenticated Encryption; Byzantine Reliable Broadcast; Diffie-Hellman; DomainKeys Identified Mail (DKIM); Key Derivation Function (KDF); Key-blinded signatures; Loopix; Nym; Response packet fragmentation; Sigma protocol

## Deniability  [concept_deniability]  (property; 6 papers)
For key exchange, deniability requires a Fake algorithm to generate a transcript and session key indistinguishable from an honest run, so a distinguisher cannot infer Bob’s involvement. The chunk concerns offline deniability unless otherwise stated.
Papers: 2009_goldberg_mpotr, 2019_tyagi_messagefranking, 2021_hashimoto_pq_x3dh_deniable, 2023_wang_notry, 2024_fiedler_pqxdh_deniability, 2026_jarecki_x3dh_sas
- assumes: Fundamental Problem of Deniability

## Cryptographic hash  [concept_hash_function]  (primitive; 7 papers)
Hashes of bulk ciphertexts and messages are included in shuffled descriptors so members and the target can detect incorrect transmissions and verify message integrity.
Papers: 2010_corrigangibbs_dissent, 2020_alwen_mls_insider, 2022_hagen_contactdiscovery, 2023_auvolat_basalt, 2024_brorsson_consistency_or_die, 2024_len_elektra, 2024_nist_fips205
- compares_with: Private Set Intersection (PSI) protocol
- uses: Global salt; Key stretching

## NDN  [concept_ndn]  (system; 7 papers)
NDN is one of the cited content-centric network proposals. The paper presents multicast as a way to adjust replication strategies in named-data networking and notes the polling burden when accessing continuous content packet by packet.
Papers: 2012_schmidt_why, 2013_chen_reliable, 2017_wang_copsslite, 2018_gundogan_hopp, 2018_kurihara_ndnreplicating, 2019_petersen_bluetoothmesh, 2023_papadakis_comdexcontext
- implements: ICN Friend design
- measures: NDN lower traffic load
- requires: CCN packet polling
- uses: NDN in-network content cache; PIT aggregation

## Discrete Logarithm Problem  [concept_discrete_logarithm_problem]  (assumption; 8 papers)
Given points, finding n such that P1=nP2 is described as computationally hard; scalar multiplication nP is straightforward and serves as a one-way function.
Papers: 2016_hopwood_zcash_protocol_spec, 2019_chase_signal_private_groups, 2019_tyagi_messagefranking, 2020_alonso_zerotomonero, 2022_newman_spectrum, 2024_collins_dr_tight, 2024_hansen_ocash, 2025_chu_signalingmalicious
- requires: Computational binding

## ECIES  [concept_ecies]  (protocol; 7 papers)
Zerocash specified ECIES for in-band secret distribution. The text notes ECIES variants permit at least 576 combinations of options and algorithms across four standards, creating underspecification.
Papers: 2016_hopwood_zcash_protocol_spec, 2017_pybitmessage_repo_protocol_docs, 2018_recabarren_tithonus, 2019_malina_secure, 2021_duguey_thesis, 2021_vac_waku2_payload_spec, 2022_vac_waku2_x3dh_spec
- hides: Message metadata
- implements: ECIES message fields
- provides: Authenticated encryption with associated data
- requires: Ciphertext padding
- uses: AES-256-CBC; DHIES; ECDH; HMAC-SHA256; SHA-512; secp256k1

## ChaCha20-Poly1305  [concept_chacha20_poly1305]  (primitive; 8 papers)
A symmetric cipher used for transaction memos and note payloads. The memo key is randomly generated; note payload keys derive from a shared secret and ephemeral public key.
Papers: 2016_hopwood_zcash_protocol_spec, 2017_grubbs_franking, 2021_len_partitioningoracle, 2022_barnes_rfc9180, 2022_penumbra_fmd_spec, 2022_penumbra_protocol_detection_memo, 2022_zip231_memo_bundles, 2026_ndolo_bitcoinv2transport
- compares_with: GCM equal-tag receiver-binding attack
- uses: Key multi-collisions; Poly1305; Zeros-check transform

## AsynchroMix  [concept_asynchromix]  (system; 3 papers)
An asynchronous MPC mixing service that selects client inputs by epoch and publishes a permutation independent of input order. It provides anonymity and availability when preprocessing is sufficient and adversarial collusion is limited to t < n/3.
Papers: 2019_lu_asynchromix, 2020_abraham_blinder, 2023_sasy_sokmetadata
- assumes: Asynchronous network adversary; Message size; Mixing collusion limit
- compares_with: Anonymity Trilemma; DC-net; MCMix; Mixnet; PowerMix; Switching network
- implements: Mix epoch input selection
- measures: Error correction delay; Measured mixing throughput; Overall message cost
- proves: Availability bound
- provides: Anonymity; Asynchronous extension; Availability; Canonical output order; Switching random permutation
- requires: Asynchronous Byzantine fault bound; Fault reserve depletion; Offline reserve buffer; Preprocessed client masks
- uses: Client input blinding; CommonSubset; HoneyBadgerMPC; PowerMix; PowerMixing; Preprocessing buffer; Reliable broadcast; Switching network

## Katzenpost  [concept_katzenpost]  (system; 6 papers)
A network assumed to operate independently; PANORAMIX helps administrators launch software with network configuration and review and consent to network parameters. Its node identity is part of its core functionality, so PANORAMIX registration is not used.
Papers: 2019_panoramix_d44, 2025_infeld_echomix, spec_katzenpost_kemsphinx, spec_katzenpost_mixdecoy, spec_katzenpost_mixnet, spec_katzenpost_pigeonhole
- assumes: Strategic packet-loss n-1 attack
- contradicts: Registration service
- instance_of: Mixnet
- provides: Forward Secrecy; No delivery guarantees
- requires: Katzenpost configuration parameters
- uses: Epoch; Epoch duration; Layered topology; Loopix; PQ Noise; Sphinx

## Peer Scoring  [concept_peer_scoring]  (mechanism; 7 papers)
A libp2p spam defense described as prone to censorship and inexpensive attacks using millions of bots; WAKU-RLN-RELAY can use it to address invalid-proof resource exhaustion at direct neighbors.
Papers: 2020_leastauthority_gossipsub_audit, 2020_vyzovitis_gossipsub_v11_evaluation, 2022_taheri_spam_protected_gossip, 2022_taheri_waku_rln_relay, 2025_farooq_staggering, 2026_kumar_lean_gossip, 2026_trinh_gossipsub_das
- attacks: Sybil Attack
- compares_with: WAKU-RLN-RELAY
- defends_against: Eager mesh forwarding; Malicious IHAVE suppression
- implements: Delivery penalty recovery
- measures: Message learning and peer score asymmetry; Peer prune measurement gap
- provides: Covert flash mesh recovery; Slot duplication stabilization; v1.1 more resistant than v1.0

## Statistical Disclosure Attack (SDA)  [concept_statistical_disclosure_attack]  (attack; 6 papers)
Estimates a user's sending behavior by combining receiver-set observations across rounds. The original form assumes at most one message per round and uniform background traffic; later variants handle multiple messages and nonuniform backgrounds.
Papers: 2013_oya_sda_family, 2016_galteland_cmixattacks, 2016_hayes_tasp, 2021_martiny_sealed_sender, 2023_brigham_sealed_sender_groups, 2024_infeld_mixnetreview
- attacks: Anonymity Set; Loop traffic receiver-cover limitation; Mix networks
- extends: Group SDA against Bob; SDA0 estimator
- instance_of: Target random epoch SDA
- provides: Identification after few messages; Sender profile
- requires: Original SDA assumptions

## Anonymous communication system (ACS)  [concept_anonymous_communication]  (system; 7 papers)
ACSs aim to make network traffic indiscernible and provide anonymity and ideally unobservability. Encryption protects content, while traffic analysis can still reveal information about communicating parties.
Papers: 2016_hayes_tasp, 2018_shirazi_survey_routing_anon, 2019_kuhn_privacynotions, 2021_len_partitioningoracle, 2022_shirali_dcnetsurvey, 2024_gregoire_onionfranking, 2026_arunachalaramanan_pirsurvey
- instance_of: DC-net; Mixnet; Onion Routing
- motivates: Abuse reporting
- provides: Private Information Retrieval; Unobservability
- requires: Observable decryption result
- uses: Distributed Hash Table

## Shor's algorithm  [concept_shors_algorithm]  (primitive; 7 papers)
The quantum algorithm used here to solve ECDLP; the paper reports circuits for 256-bit ECDLP using 1,200 logical qubits and 90 million Toffoli gates, or 1,450 logical qubits and 70 million Toffoli gates.
Papers: 2017_bindel_transition_pki, 2018_aggarwal_quantum_bitcoin, 2018_bindel_hybrid_kem_ake, 2024_rial_outfox, 2025_driscoll_rfc9794, 2025_gidney_rsa_million_qubits, 2026_babbush_ec_crypto_quantum
- attacks: RSA; RSA-OAEP; Sphinx; secp256k1
- provides: Unprocessed transaction theft
- requires: Cryptographically Relevant Quantum Computer (CRQC)
- uses: Paper’s truncated residue accumulation

## NTRU assumption  [concept_ntru]  (assumption; 6 papers)
The paper concludes NTRU is anonymous and collision-free in the QROM under strong disjoint-simulatability of its deterministic underlying PKE; its hybrid PKE can be anonymous and robust with an appropriate DEM.
Papers: 2017_polyakov_prepubsub, 2018_aggarwal_quantum_bitcoin, 2021_agrawal_lattice_blind_sig, 2022_xagawa_anonymitykems, 2023_beullens_lattice_blind_sig, 2026_basso_kopis
- assumes: Modified DSPR assumption; Modified PLWE assumption; NTRU key generation cost; Strong disjoint-simulatability
- proves: Tight reductions
- provides: ANON-CCA security; SCFR-CCA security; SROB-CCA security; SSMT-CCA security
- requires: FROB security
- uses: NTRU-DPKE; SXY

## Cuckoo hashing  [concept_cuckoo_hashing]  (primitive; 7 papers)
With w independent hash functions, each item has w candidate buckets. If all are occupied, the algorithm randomly evicts an item and recursively reinserts it, up to a maximum number of iterations.
Papers: 2018_angel_sealpir, 2018_demmler_pirpsi, 2019_ali_pircommcomp, 2023_patel_keywordpirsparse, 2024_burton_respire, 2024_decastro_whispir, 2026_mukam_byzantineresilient
- compares_with: SparsePIR response-size reduction
- provides: Batch correctness error; Random-hash bucket size
- requires: Batch bucket capacity choice

## Quasar  [concept_quasar]  (protocol; 2 papers)
An anonymous group authenticated messaging protocol with tracing soundness. Its theorem claims signing correctness, global state-update correctness, non-colluding unforgeability, anonymity, anonymous blocklisting, and tracing soundness under the listed primitive assumptions.
Papers: 2011_mega_dissemination_decentralized, 2025_hashimoto_mls_app_auth
- assumes: KEM IND-CCA assumption; MAC sEUF-CMA security; OWF one-wayness assumption; PRF pseudorandomness assumption; PRP pseudorandomness assumption
- compares_with: COSMAC; One-time signatures in STARS; Piggybacked message histories
- extends: Active subgroup G
- measures: QUASAR communication result; QUASAR online upload result
- provides: Anonymous blocklisting; Global state-update correctness; Tracing soundness; User traceability
- requires: Global state updates; Token budget T
- uses: Bloom Filter; COSMAC; Epoch PRP token shuffling; One-time tokens; PRF seed; Per-recipient seed encapsulation; Private per-recipient token; Public token database DB; Public token one-way image

## XMSS  [concept_xmss]  (primitive; 6 papers)
XMSS is the concrete KES instantiation used for a rough performance estimate, with SHA-256 and 128-bit security. Its reported signature verification time is 0.3 ms.
Papers: 2018_aggarwal_quantum_bitcoin, 2019_bernstein_sphincsplus, 2020_schwabe_kemtls, 2024_brorsson_consistency_or_die, 2024_nist_fips205, 2025_drake_leansig
- compares_with: Equal quantum-security length comparison
- extends: WOTS+
- instance_of: Key Evolving Signatures
- provides: XMSS message capacity; XMSS signature size
- requires: Hash random oracle assumption; WOTS+
- uses: Incomparable encoding; Merkle hash tree; WOTS+

## Spiral  [concept_spiral]  (protocol; 5 papers)
A follow-up work adopting the OnionPIR paradigm. It uses a log(q)/log(t) ratio of about 8 in the comparison discussed here and proposes separate decomposition parameters for query unpacking and later dimensions.
Papers: 2022_menon_spiral, 2023_lazzaretti_treepir, 2023_patel_keywordpirsparse, 2024_burton_respire, 2025_chen_onionpirv2
- compares_with: Million-record communication result
- extends: OnionPIR
- implements: Server folding
- measures: Plaintext dimension trade-off; SPIRAL recursion cost; Spiral comparison
- proves: Correctness parameter bound
- provides: Modulus trade-off; PIR query privacy; Single ciphertext query
- uses: Database hypercube; GSW encoding; Modulus switching; Regev encoding

## Tagging attack  [concept_tagging_attack]  (attack; 6 papers)
An attacker modifies traffic characteristics at one circuit endpoint to recognize it at another and de-anonymize communication. An example rendezvous-point attack sends 50 PADDING cells followed by a DESTROY cell.
Papers: 2009_danezis_sphinx, 2016_galteland_cmixattacks, 2017_chaum_cmix, 2017_kim_sgxtor, 2018_degabriele_untagging_tor, 2026_auerbach_anonauthkem
- attacks: cMix
- compares_with: Traffic Analysis
- implements: XOR tagging
- instance_of: Last-node tag attack
- uses: Circuit teardown amplification

## UDP  [concept_udp]  (protocol; 8 papers)
The transport protocol used by the proposal. The paper says UDP has smaller headers than TCP, is compatible with multicast, and avoids unnecessary transport feedback for applications that do not need end-to-end reliability.
Papers: 2011_malekpour_endtoend, 2013_davis_improvingpacket, 2018_anon_publishsubscribe, 2019_patra_leveragingpublish, 2019_rohrer_kadcast, 2021_abegg_supra, 2023_peeroo_survey, 2026_choi_roswhen
- improves_on: TCP constraints in WSN
- requires: RaptorQ

## Discrete logarithm assumption  [concept_discrete_logarithm_assumption]  (assumption; 8 papers)
The KeyRoll instantiation assumes the discrete logarithm problem is hard in a prime-order group G; this supports unpredictability and one-wayness on the second input.
Papers: 2012_libert_anonymousbe, 2019_sonnino_coconut, 2022_cong_key_lattice, 2023_agrawal_traceablemixnets, 2023_kovacs_umbra_anonymity, 2023_tessaro_bbs, 2025_chairattana_everlasting_tokens, 2026_bao_x3dh_tight

## Group signature  [concept_group_signature]  (primitive; 6 papers)
A group manager registers users and issues certificates; a user signs anonymously for the group, with signatures publicly verifiable and traceable only by the specified group tracer, including against the manager.
Papers: 2013_vansaberhagen_cryptonote, 2018_liu_keyinsulatedstealth, 2019_chase_signal_private_groups, 2023_lai_commit_transferrable_sig, 2024_argo_pq_signatures_privacy, 2025_hashimoto_mls_app_auth
- attacks: GAM and GS group-scope mismatch
- compares_with: Derived-key privacy; Sealed Sender
- extends: Ring signature
- instance_of: Orca
- provides: Anonymity; Tracing soundness; User traceability
- requires: Verifiable encryption
- uses: Commit-Transferrable Signature (CTS); Group signature flow

## SealPIR  [concept_sealpir]  (system; 5 papers)
The PIR engine used in the modified Pung deployment. It reduces XPIR's network cost with modest additional computation; in the reported comparison it contributes to 3.1× higher throughput at k=64 when combined with mPIR.
Papers: 2018_angel_sealpir, 2019_ali_pircommcomp, 2022_davidson_frodopir, 2022_menon_spiral, 2023_ahmad_pantheon
- assumes: Benchmark platform
- compares_with: Large database CPU tradeoff
- extends: XPIR
- instance_of: Private Information Retrieval
- measures: SealPIR response-time reduction; SealPIR server CPU overhead; SealPIR throughput comparison
- provides: Response overhead; SealPIR query-size savings; Server computation throughput
- uses: Oblivious query expansion

## Kadcast  [concept_kadcast]  (protocol; 2 papers)
A structured overlay broadcast protocol for blockchain block propagation. In a 1,000-node cloud testbed it delivered blocks 43% faster on average than Bitcoin Core header-based propagation and 27% faster than Bitcoin Core with compact block relay.
Papers: 2019_rohrer_kadcast, 2021_rohrer_kadcast_ng
- compares_with: Erlay; Graphene; Traffic Analysis; VanillaCast; Velocity
- defends_against: Denial of service attack; Eclipse Attack
- extends: Kademlia
- implements: IP-derived node identifiers; REQUEST_BLOCK recovery
- instance_of: Publish/Subscribe
- measures: Bitcoin-like propagation speedup; Ethereum-like stale block result
- provides: Kadcast broadcast complexity; decentralization preservation; overlay and dissemination control
- uses: Broadcast redundancy β; Compact blocks; FEC overhead factor f; IP binding and cryptographic puzzles; Kademlia; Parallel route selection; RaptorQ; Stable-node bucket eviction; UDP; Validate blocks before forwarding

## Respire  [concept_respire]  (protocol; 3 papers)
A lattice-based, single-server PIR scheme for small records. For over one million 256-byte records it uses 6.1 KB online communication; reported throughput is 200–400 MB/s.
Papers: 2024_burton_respire, 2025_chen_onionpirv2, 2026_li_letopir
- assumes: Batched correctness assumptions; RLWE assumption
- extends: Spiral
- instance_of: Private Information Retrieval; Single-server architecture
- measures: Batch communication result; Batch computation overhead; Hint size comparison; Million-record communication result; Response time cost; Throughput comparison
- provides: PIR scope; Query privacy
- requires: Small record setting
- uses: Batch Codes; Client hint model; GSW Encryption; Query Compression; Query packing; RLWE Encoding; RLWE assumption; Response Compression; Response compression; Ring Switching

## EROR  [concept_eror]  (protocol; 3 papers)
A repliable onion packet format built from symmetric-key primitives and public-key encryption. It prevents forward payload tagging and is designed to retain request-reply indistinguishability with payload size at most twice Sphinx and packet processing about twice as fast as Sphinx.
Papers: 2024_klooss_eror, 2024_rial_outfox, 2026_coijanovic_omnisphinx
- assumes: DLR$-CPA security; Global adversary colluding with receiver and relays; IND-CCA; Integrated system model; PRF security; SUF-CMA security
- compares_with: Speedup over prior schemes; Sphinx
- defends_against: Payload tagging attack
- implements: Separate payload parts with dummy data
- improves_on: Succinct Non-Interactive Arguments; Updatable Encryption
- leaks: Active tagging attack
- measures: Onion creation speed; Packet processing speed; Payload size overhead
- proves: End-to-end reply integrity requirement
- provides: Backward payload end-to-end integrity; Forward payload integrity; Request-reply indistinguishability; Strong backward layer-unlinkability; Strong forward layer-unlinkability
- requires: Fixed maximum path length; Header-based duplicate detection
- uses: Ephemeral keys; Random onion replacement on honest subpaths; Symmetric-key primitives and public-key encryption

## Sender anonymity  [concept_sender_anonymity]  (property; 6 papers)
A corrupted recipient colluding with the server should not determine which of two uncorrupted senders sent a message. The security game permits all recipients and the server to be corrupt and up to η−2 senders corrupt.
Papers: 2013_gelernter_limits_provable_anonymity, 2014_backes_mator, 2015_barroso_adtn, 2016_angel_pung_1, 2021_das_divide_and_funnel, 2025_das_spar
- instance_of: Unlinkability
- proves: FHE security parameter

## Sigma protocol  [concept_sigma_protocol]  (protocol; 7 papers)
Used to prove sender knowledge of uploaded ciphertexts and mix-server knowledge of homomorphic blinding factors. The chunk estimates equality and range proofs would keep sender-side costs below 1 second per sender.
Papers: 2014_chase_algebraicmacs, 2015_unger_sok_securemessaging_tr, 2019_tyagi_messagefranking, 2021_duguey_thesis, 2023_agrawal_traceablemixnets, 2023_kocaogullar_pudding, 2026_draft_act
- defends_against: Authenticated Diffie-Hellman AKE
- provides: Zero Knowledge
- uses: Key-blinded signatures

## IND-CCA security  [concept_ind_cca_security]  (property; 5 papers)
The stated FHE security notion means an adversary cannot distinguish encryptions of chosen messages; ciphertexts reveal no information beyond their length. In sPAR this protects client inputs from a semi-honest server observing ciphertexts.
Papers: 2020_bellare_imessage_signcryption, 2022_maram_pq_anonymity_kyber, 2024_barbosa_xwing, 2024_rial_outfox, 2025_das_spar
- assumes: Quantum random oracle model
- compares_with: FO⁶⊥m transform; Injectivity assumption gap
- proves: Theorem 1 IND-CCA bound
- requires: δ-correctness
- uses: IND-CPA security; Quantum random oracle collision resistance

## SUF-CMA security  [concept_suf_cma]  (assumption; 7 papers)
Strong unforgeability under chosen-message attack is assumed for signatures in the ETKPSK authenticity result; the reduction embeds a challenge public key and uses its signing oracle.
Papers: 2021_kuhn_onion_replies, 2022_grubbs_anonrobustpq, 2023_balbas_sender_keys, 2024_collins_k_waay, 2024_klooss_eror, 2025_cremers_etk, 2026_chu_anamorphic
- defends_against: Authenticity violation
- uses: IND$

## Pseudorandom function (PRF)  [concept_prf]  (primitive; 6 papers)
The constructions use a PRF with domain-separated labels for derived keys, tags, and authentication values; the tagging security analysis models the PRF as a random oracle for its lower-bound discussion.
Papers: 2022_hashimoto_mls_metadata, 2022_ishibashi_pq_osake, 2023_auerbach_pcs_cost_concurrent, 2025_gunther_hybrid_obfuscated_kex, 2025_hashimoto_mls_app_auth, 2026_auerbach_anonauthkem
- uses: Explicit authentication bound; Probing resistance bound; Test case security hops

## Hydra  [concept_hydra]  (protocol; 2 papers)
A padded-circuit mix network supporting contact discovery, messaging, and dialing with strong anonymity and relatively low latency. It uses symmetric cryptography during an epoch; benchmarks report processing messages an order of magnitude faster than strong-anonymity messaging systems, with comparable bandwidth overhead.
Papers: 2022_schatz_hydra, 2024_coijanovic_pirates
- assumes: Global external attacker; Malicious system entities; Reliable entity links
- extends: Onion Routing
- improves_on: Cryptography benchmark speed
- instance_of: Mixnet
- provides: Location anonymity; Offline message storage; Relationship anonymity
- requires: Synchronized epochs
- uses: Cell onion encryption; Contact service; Dummy cells; Dummy circuits; Out-of-band shared secret; Padded circuits; Per-epoch mix keys; Publish/Subscribe; Random subscription waits; Rendezvous Point

## Key-Policy Attribute-Based Encryption (KP-ABE)  [concept_key_policy_attribute_based_encryption]  (protocol; 2 papers)
Messages are encrypted under a set of attributes; a private key is generated for an access policy over a subset of attributes. Policies can be chosen after encryption, and ciphertext/public keys can be homomorphically evaluated by a third party.
Papers: 2023_abdennebi_latticebased, 2023_abdennebi_latticepubsub
- assumes: RLWE assumption; Ring learning with errors; Shortest Vector Problem (SVP)
- compares_with: Proxy Re-Encryption (PRE)
- instance_of: Attribute-Based Encryption; Lattice-based cryptography
- provides: Attribute-based search; End-to-end message confidentiality; Subscriber-interest privacy
- uses: Homomorphic ciphertext and public-key evaluation

## Public-key infrastructure  [concept_public_key_infrastructure]  (assumption; 7 papers)
The modeled PKI lets any user request a fresh encryption public key for another ID, records (pk, sk, ID), and gives that information to the attacker. The key owner can request the corresponding secret key; each public key is used only once.
Papers: 2009_danezis_sphinx, 2018_chase_seemless, 2020_dias_mqttmecanismo, 2021_javani_aot, 2024_bhargavan_pqxdh, 2026_tang_dumbomix, iog_security_analysis_and_improvements_for_the_ietf_mls_standard
- compares_with: Untrusted key distribution server
- defends_against: Distributed Hash Table
- implements: One-use public keys
- provides: Authentication, integrity, and non-repudiation

## Pastry DHT  [concept_pastry]  (protocol; 7 papers)
Pastry uses 128-bit node identifiers generated by hashing, ring organization and segmented routing tables. The chunk states a routing table size of (2b−1)log₂(N) and lookup hops of log₂(N).
Papers: 2012_setty_poldercast, 2013_rene_erreichen, 2014_pellegrino_pushingdynamic, 2015_kermarrec_want_centralized, 2016_royer_content, 2016_royer_routagebase, 2023_jami_swarm_drt_docs
- instance_of: Distributed Hash Table
- measures: Pastry lookup hops
- provides: Limited notification cost; Pastry routing table size; Scribe degree bound
- requires: Pastry b parameter
- uses: Pastry forwarding

## Secret Sharing  [concept_secret_sharing]  (primitive; 5 papers)
A (t,m)-perfect secret-sharing scheme divides quarantine secrets into shares. Compromise of at least t shareholders from different share families during their shared critical windows can compromise the challenge group key.
Papers: 2013_yoon_adaptation_techniques, 2020_das_beyond_mixnets, 2021_mazmudar_you, 2023_chevalier_quarantined_treekem, 2025_lebrun_thesis
- defends_against: Verification-key compromise
- hides: Quarantine initiator
- implements: Availability and integrity mechanisms
- provides: Ghost recovery; Resistance to compromised relays; Share recovery
- requires: Threshold security and availability trade-off

## Pseudo Random Function  [concept_pseudo_random_function]  (primitive; 7 papers)
The paper uses a PRF to derive two randomness values from one client ephemeral secret; the function family should be indistinguishable from a truly random function to PPT distinguishers, up to negligible advantage.
Papers: 2016_hopwood_zcash_protocol_spec, 2017_piotrowska_annotify, 2018_bhargavan_treekem, 2020_bienstock_group_ratcheting_concurrency, 2021_hashimoto_pq_x3dh_deniable, 2022_ishibashi_pq_osake, 2025_bowe_noteonnotes
- compares_with: Key Encapsulation Mechanism
- implements: Epoch-specific notification identifier; Single client ESK
- requires: Collision Resistance
- uses: Independent proof statements; Upper bound O(t·(1+log(n/t)))

## HOPR  [concept_hopr]  (protocol; 3 papers)
A decentralized metadata-private messaging protocol for communication between networks, applications, and users. It adds a paid multi-hop message layer above a P2P layer such as libp2p or WebRTC and supports TCP/IP or QUIC underneath.
Papers: 2019_burgel_hopr, 2021_diaz_nym, 2026_janjua_tor_validators
- attacks: Eclipse Attack; First-Spy Estimator
- compares_with: Matrix
- instance_of: Mixnet
- leaks: HOPR Payment Information Leakage; Peer Address Enumeration
- provides: Low-resource cryptography objective; Metadata Privacy; Network scale estimate; Open membership; Receiver anonymity; Sender anonymity; Sender-receiver unlinkability
- requires: Payment channel design requirements
- uses: Bootstrap-node routing; Chaumian mixnet; Ethereum; HKDF; Mixnet; Multi-hop paid relay; Onion Routing; Packet caching and shuffle; Payment channel; Proof-of-Relay

## Asymmetric Message Franking (AMF)  [concept_asymmetric_message_franking]  (primitive; 4 papers)
Lets a recipient report abusive content while retaining end-to-end privacy by default; a moderator can identify the source of a verified reported message, while its knowledge is non-transferable. Hecate adds preprocessing, source tracing, and forward and backward security.
Papers: 2019_tyagi_messagefranking, 2021_issa_hecate, 2023_eskandarian_abusereporting, 2024_gregoire_onionfranking
- assumes: Discrete Logarithm Problem; Knowledge-of-Exponent Assumption (KEA)
- defends_against: Compromised moderation infrastructure
- implements: AMF proof relation; Seven-algorithm AMF syntax
- improves_on: Designated-verifier signatures
- motivates: Designated-verifier signatures
- proves: Gap Diffie-Hellman assumption
- provides: Accountability; Cryptographic deniability; Metadata-private messaging
- uses: Fiat-Shamir heuristic; Non-interactive zero-knowledge proof of knowledge; Signature of knowledge; Signatures of knowledge

## Trellis  [concept_trellis]  (protocol; 3 papers)
An anonymous broadcast protocol following cMix to decouple setup from broadcast; messages from the same user remain linkable at the last mixnode layer unless expensive setup runs after every broadcast round.
Papers: 2021_das_divide_and_funnel, 2023_langowski_trellis, 2023_sasy_sokmetadata
- assumes: Differential Privacy; Malicious server fraction f
- implements: One-time path establishment; Random routing mix-net; Repeated anonymous broadcast
- instance_of: Mixnet; SUBS
- measures: Networked deployment evaluation
- proves: ART security under gap CDH; Mixing analysis with malicious servers
- provides: Availability guarantee; Dishonest-majority reconfiguration; Metadata Privacy; Publish/Subscribe; Sender anonymity; Server churn and elimination
- requires: Cryptographic assumptions; Synchronous communication; User liveness
- uses: Anonymous Routing Tokens (ART); Anonymous routing tokens; Boomerang Encryption (BE); Boomerang encryption; On-demand blame and recovery; Public bulletin board; Trellis blame and recovery

## WhisPIR  [concept_whispir]  (protocol; 2 papers)
Stateless PIR protocol using homomorphic encryption; clients need only a few dozen milliseconds for key generation, encryption, and decryption. The paper reports 128-bit security for its parameters.
Papers: 2024_decastro_whispir, 2025_chen_onionpirv2
- compares_with: Computation comparison; HintlessPIR comparison; SimplePIR; SimplePIR comparison; Spiral comparison; Stateless communication comparison
- improves_on: Evaluation key upload
- instance_of: Private Information Retrieval
- measures: Large database scaling
- provides: Blocklist lookup privacy; Blocklist performance; Client computation cost; Communication computation tradeoff; Frequent database updates; Small public parameters
- requires: Ephemeral clients; WhisPIR setup parameters
- uses: BGV; BGV homomorphic encryption; Batched queries; Database chunking; Hypercube database representation; Index expansion; Index splitting; Iterative rotation precomputation; Non-relinearized multiplication; One-time server precomputation

## One-time signature  [concept_one_time_signature]  (primitive; 4 papers)
A one-time signature key pair (SK?, VK?) is generated for the challenge, and the signature covers the ciphertext components; strong unforgeability bounds transitions that remove the verification-key rejection rule.
Papers: 2012_libert_anonymousbe, 2014_bensasson_zerocash, 2018_poettering_asynchronous_rke, 2025_hashimoto_mls_app_auth
- defends_against: Pour transaction malleability
- leaks: Anonymity
- requires: Strong unforgeability

## Argon2  [concept_argon2]  (system; 4 papers)
A memory-hard hashing scheme designed to fill memory quickly, use parallel computing units, and resist time-memory tradeoffs. It targets password hashing, key derivation, cryptocurrencies, and other applications.
Papers: 2016_biryukov_argon2, 2016_biryukov_equihash, 2021_len_partitioningoracle, 2022_hagen_contactdiscovery
- extends: Argon2d; Argon2i
- implements: Parallel lanes and slices
- improves_on: Hash reversal cost increase; Time-area product
- measures: Memory fill rate
- provides: Memory-hardness model; Parallelism limit
- requires: Argon2 input parameters
- uses: Argon2 block size

## PrivCount  [concept_privcount]  (system; 2 papers)
A distributed measurement system with a tally server, at least one data collector, and at least one share keeper. It reports noisy event counts and provides (ϵ, δ)-DP if at least one share keeper is honest.
Papers: 2016_jansen_safely_measuring_tor, 2018_mani_tor_usage_privacy_preserving
- assumes: PKI assumption
- extends: PrivEx; S2
- instance_of: PrivCount deployment; Tor
- measures: Aggregated relays; Connected and active users; Exit policy affects traffic type; Research deployment contributors; Web traffic share
- provides: Differential Privacy
- requires: Action bounds; Honest share-keeper condition; Reconfiguration delay
- uses: Circuit activity thresholds; Client IP map retention; Collection round durations; Data collector; Differential Privacy; Exit-port traffic classification; Interactive statistics omitted; Measurement deployments; Measurement noise and confidence intervals; PRIVCOUNT event extension

## Man-in-the-Middle Attack  [concept_man_in_the_middle_attack]  (attack; 7 papers)
Because Android uses a permissive trust manager for seed-node HTTPS, a malicious DNS operator or Internet Access Provider can substitute a rogue seed node and service node, redirecting clients to an attacker-controlled Lokinet network. The report demonstrated redirection with Frida-hooked DNS-poisoning emulation.
Papers: 2016_lazar_alpenhorn, 2017_bos_kyber, 2019_malina_secure, 2020_pozo_evaluation, 2021_quarkslab_session_audit, 2022_albrecht_bridgefy_again, 2026_gajji_blockchainenabled
- leaks: No peer key verification
- provides: Rogue network control

## Oblivious pseudorandom function (OPRF)  [concept_oblivious_pseudorandom_function]  (primitive; 5 papers)
The server holds PRF key k and the user supplies input x; the user learns F_k(x), while the server learns nothing about x. The construction uses elliptic curve techniques.
Papers: 2018_davidson_privacypass, 2019_kales_contactdiscovery, 2023_rfc9497_oprf, 2024_jia_homerun, 2024_rfc9578_privacypass_issuance
- defends_against: Identity element rejection
- provides: Client learns no private key; Server input and output privacy; VOPRF token parameters
- requires: Informational RFC status; Input size limit; Prime-order group assumption
- uses: Blinded client input; Client unblinding and finalization; HashToGroup mapping; Server key evaluation; Two-message client-server exchange

## Rate Limiting Nullifiers (RLN)  [concept_rln]  (primitive; 4 papers)
An extension of Semaphore using (2,n)-Shamir secret sharing: a second signal for one external nullifier exposes enough information to reconstruct the sender's identity key, enabling removal and financial punishment.
Papers: 2021_vac_waku2_rln_relay_spec, 2022_taheri_waku_rln_relay, 2025_logos_mix_dos_protection, 2025_logos_mix_dos_rln
- defends_against: Sybil Attack; Well-formed packet spam
- extends: Semaphore
- instance_of: Pluggable DoS protection framework
- provides: Epoch rate limit
- requires: Membership tree synchronization; Private global state access; Proof-generation computation cost; RLN group membership requirement
- uses: Identity commitment; Identity commitment tree; Identity key share; Internal nullifier; Shamir secret sharing; zk-SNARK

## PQ3  [concept_pq3]  (protocol; 4 papers)
PQ3 combines a symmetric ratchet, P-256 ECDH ratchet, and ML-KEM-1024 ratchet. Its symmetric chain uses 256-bit keys and HKDF-SHA384, has no chain-length limit, and is assessed here at 64-bit classical security.
Papers: 2024_linker_imessage_pq3, 2024_mattsson_symmetric_ratchets, 2024_stebila_pq3_analysis, 2026_chu_anamorphic
- assumes: Active network adversary
- compares_with: Session handling transfer open question
- extends: Enhanced cryptographic primitive models; IDS key roll-over extension
- implements: Asymmetric ratchet; Initial key establishment; Symmetric ratchet
- instance_of: ρ-chain
- proves: Correctness results; Incoming ratchet key indistinguishability; Initiator initial key indistinguishability; Outgoing ratchet key indistinguishability; PQ3 ciphertext hybrid bound; Responder initial key indistinguishability
- provides: PQ3 bandwidth; PQ3 ratchet parameters; Public formal artifacts; Quantum resilience claim
- uses: ML-KEM; Message authentication; Multi-Stage AKE Security Model; Tamarin

## SLH-DSA  [concept_slh_dsa]  (protocol; 2 papers)
Stateless hash-based signature standard based on SPHINCS+, designed to resist attacks from a large-scale quantum computer. It relies on preimage resistance and related properties of hash functions.
Papers: 2024_nist_fips205, 2026_mallick_aquaman
- assumes: Hash security properties
- contradicts: Floating-point arithmetic
- defends_against: Fault attack; Multi-target attack; Side-Channel Attack
- implements: Root-based signature verification
- instance_of: SPHINCS+
- provides: Approved parameter sets; Digital signature properties; Large-scale quantum resistance; Public key components; Signature composition; len2 value
- requires: Approved random bit generator; Private key components; Private key regeneration check; Private key secrecy; Public key length check; Sensitive intermediate data destruction; Signature identity assurances; Standalone component interface restriction
- uses: ADRS address format; Cryptographic hash; FORS; Hypertree; Pseudorandom function; Randomized message hash; WOTS+; XMSS

## ntor  [concept_ntor]  (protocol; 5 papers)
Tor's deployed 1W-AKE uses classical DH assumptions. The chunk says it is not forward-secure against future quantum attacks and gives HybridOR a roughly 33% computation improvement over it.
Papers: 2012_backes_provably_secure_onion, 2013_tor_prop224_rendng, 2015_ghosh_pq_onion, 2015_zhang_tor_quantum_handshake, 2016_tor_proposal_263_ntru_handshake
- attacks: Quantum attack on classical DH
- compares_with: Handshake bandwidth
- instance_of: 1W-AKE requirements; ntor extra-data handshake
- leaks: Harvest-then-decrypt attack
- measures: Handshake computation time
- provides: Anonymity; Forward Secrecy; One-way anonymity; One-way authentication

## W HATS U P  [concept_whatsup]  (system; 1 papers)
A decentralized instant news recommender with no central authority, using implicit user interests and heterogeneous gossip to deliver relevant news.
Papers: 2013_boutet_whatsup_decentralized
- assumes: Privacy scope
- compares_with: C-Pub/Sub; Centralized comparison; Topic-Based Pub/Sub
- defends_against: Content bombing limitation
- implements: Implementation and deployment
- improves_on: Recall versus cascading
- measures: Dissemination hop distribution; Experiment setup; Interest change convergence; Join convergence cycles; Message loss results; News bandwidth cost; PlanetLab low fanout recall; PlanetLab setup; Survey best-performance results; Survey comparison results
- provides: Interest change quality floor; Joining node precision; Privacy scope; Publish/Subscribe; Robustness to message loss
- requires: Private profile dissemination challenge; TTL dissemination threshold
- uses: B E E P; B EEP (Biased EpidEmic Protocol); Dislike mechanism; Profile obfuscation; Proxy anonymization; Sociability definition; W UP

## Dining Cryptographers Network (DC-Net)  [concept_dining_cryptographers_network]  (protocol; 3 papers)
DCN-based anonymous communication aims for unconditional unobservability and provable traffic-analysis resistance, with high computation and communication overhead and limited scalability. Recent enhancements can reduce latency, computation, and communication costs compared with the original DCN.
Papers: 2013_zamani_anonymousbroadcast, 2017_barman_prifi, 2022_shirali_dcnetsurvey
- assumes: DCN strong attacker model
- attacks: DCN churn failure; DCN slot collisions; Denial of service attack
- defends_against: Traffic Analysis
- extends: Multi-round arbitrary-length messages
- implements: DCN XOR cancellation
- instance_of: Anonymous communication system (ACS)
- measures: DCN Overhead and Scalability; DCN scaling costs
- motivates: Blockchain Dissemination Privacy Gap
- provides: DCN non-interactivity; DCN unobservability set; Unobservability
- requires: DCN key exchange assumption

## Module-LWE  [concept_module_lwe]  (assumption; 7 papers)
A structured LWE variant over modules of a polynomial ring that generalizes Ring-LWE and allows flexible dimensions to balance security and efficiency. The paper says it underlies Kyber and Dilithium under appropriate parameters.
Papers: 2017_bos_kyber, 2021_agrawal_lattice_blind_sig, 2023_beullens_lattice_blind_sig, 2024_liu_snakeeye, 2025_liu_mmmrkem, 2025_mikic_pqstealth, 2026_mangipudi_auditable_cgka
- attacks: Snake-eye attack
- compares_with: Module-LWR

## Silent Payments  [concept_silent_payments]  (protocol; 3 papers)
A Bitcoin protocol where a receiver publishes static scan and spend keys, while senders derive fresh payment outputs. Its scan loop tries candidate indices through Kmax and tests outputs and labels.
Papers: 2023_bip352_silent_payments, 2024_mongardini_stealthbeyond, 2026_qian_silentpayments
- compares_with: CoinJoin
- defends_against: Outside-observer linkability; SIGHASH_ANYONECANPAY; Sender privacy
- extends: Encrypted payment notification
- instance_of: BitTorrent
- provides: Address payload size; Change label zero; Independent output derivation; Labeled spend keys; No transaction overhead; Static address without notifications; Test vectors
- requires: Group size cap; Recipient blockchain monitoring; Scanning cost tradeoff; SegWit
- uses: BIP32; BIP341; Bech32m; Eligible input key sum; Elliptic-curve Diffie–Hellman; secp256k1

## Quarantined-TreeKEM (QTK)  [concept_quarantined_treekem]  (protocol; 2 papers)
A quarantine mechanism for group messaging that adds quarantine keys, secret shares, and reconnect recovery to TreeKEM. Its forward secrecy in the stated worst case falls back to original TreeKEM’s level and never below.
Papers: 2023_chevalier_quarantined_treekem, 2025_lebrun_thesis
- assumes: Partially active adversary
- compares_with: MLS
- defends_against: Ghost users
- extends: Jointly implemented quarantine; TreeKEM
- improves_on: Critical window; Forward Secrecy; Post-Compromise Security
- proves: Asynchronous CGKA security game
- provides: Inactive ghost users; Quarantined member message access; TreeKEM
- requires: Equal shareholder unavailability model
- uses: Broadcast-only setting; Default share distribution; Horizontal share distribution; Quarantine commit fields; Quarantine end proposal size; Quarantine initiator; Quarantine key count; Quarantine key update; Quarantine recovery; Quarantine secret sharing

## SparsePIR  [concept_sparsepir]  (system; 2 papers)
A single-server keyword PIR framework that encodes sparse key-value databases as linear combinations and can be built on standard PIR schemes. It has the same request and response sizes as its underlying PIR, no additional client storage, and about 2% more server computation in the reported million-entry example.
Papers: 2023_patel_keywordpirsparse, 2024_celi_keywordpir
- assumes: Single-server trust setting
- compares_with: Constant-weight comparison
- implements: Keyword PIR
- instance_of: Private Information Retrieval
- measures: Communication comparison; Response overhead; Server computation cost
- provides: Keyword PIR; Privacy leakage scope; SparsePIR encoding size; SparsePIR response-size reduction
- requires: Database re-encoding on updates
- uses: Encoding failure and resampling; FHE parameter choice; Fully homomorphic encryption (FHE); Hashed key-value representation; Offline query-independent parameters; Private Information Retrieval; Random band matrices; Random partition encoding; Recursive hypercube representation

## CoAP  [concept_coap]  (protocol; 4 papers)
Lightweight IoT protocol that can use request/response for OAuth credential requests and Publish/Subscribe for data updates. It commonly relies on UDP and DTLS; the authors report better bandwidth use and round-trip time than MQTT in cited work.
Papers: 2013_davis_improvingpacket, 2017_islam_observingiot, 2018_anon_publishsubscribe, 2020_pozo_evaluation
- implements: Protocol publication discipline; Publish/Subscribe
- provides: CoAP IP multicast groups; CoAP publication discipline
- uses: CoAP Token size; CoAP message ID; CoAP publication discipline; Fixed retransmission timeout; UDP

## ECDH  [concept_ecdh]  (primitive; 6 papers)
The sender combines destination public key K with fresh private key r to derive shared point P; the receiver combines private key k with transmitted public key R to derive the same point.
Papers: 2017_pybitmessage_repo_protocol_docs, 2019_paquin_pq_tls_benchmark, 2021_martiny_sealed_sender, 2021_tron_book_of_swarm, 2024_stebila_pq3_analysis, 2026_qian_silentpayments
- provides: Candidate-index scan; Session key
- uses: ext1 randomization

## BBS+ signatures  [concept_bbs]  (primitive; 3 papers)
A dedicated signature-based construction for anonymous credentials; BBS is described as a popular current choice, with BBS-based credentials suggested for the EUDIW and requiring pairing-friendly elliptic curves such as BN-462 or BLS12-381.
Papers: 2023_agrawal_traceablemixnets, 2023_tessaro_bbs, 2025_slamanig_privacy_auth
- assumes: q-SDH assumption
- compares_with: Cheon’s attack
- extends: Truncated BBS
- improves_on: Anonymous Credentials
- motivates: Anonymous Credentials
- proves: Algebraic Group Model; One-more unforgeability for commitments; Standard model security bound; Tight AGM security bound
- provides: Anonymous Credentials; Deterministic e option; Partial disclosure proof of knowledge; Public and secret key size comparison; Short BBS signature format
- requires: BBS signature parameters; Pairing curve hardware gap
- uses: Signing user commitments; Type-3 pairings

## HomeRun  [concept_homerun]  (protocol; 2 papers)
Oblivious Message Retrieval protocol using two non-colluding, semi-honest servers. It supports unlimited pertinent messages, periodic deletion, appending-based addition, full privacy, and request unlinkability.
Papers: 2024_jia_homerun, 2025_chu_signalingmalicious
- assumes: Two non-colluding semi-honest servers
- compares_with: Fuzzy Message Detection
- defends_against: Amplified denial-of-service attack; Pertinent-message overflow DoS
- extends: Horizontal server-pair scaling
- implements: Deletion tied to message retrieval; Periodic batch deletion; Stealth one-time address
- instance_of: Oblivious Message Retrieval
- measures: 16-thread LAN runtime; 16-thread WAN runtime; Digest size; Inter-server communication; Recipient address size; Recipient reconstruction time; Recipient request communication; Single-thread WAN runtime
- provides: Full privacy; Linear scaling in bulletin size; Recipient deletion choice; Request unlinkability; Unlimited pertinent messages
- uses: Compressed message label; Private Information Retrieval; Stealth Address

## Kachina  [concept_kachina]  (protocol; 1 papers)
Kachina is a UC-based core protocol for privacy-preserving smart contracts, using non-interactive zero-knowledge proofs and targeting the Nakamoto-consensus setting of a shifting, untrusted party set. It supports contracts that divide state into shared public state and each party’s local private state.
Papers: iog_kachina_foundations_of_private_smart_contracts
- assumes: Nakamoto consensus; Static corruption
- extends: δ-delay ledger
- hides: State oracle transcripts
- implements: Future-object polling; Transaction publication; Zerocash
- leaks: Transcript commits to ledger data at creation
- proves: Kachina UC emulation theorem; UC emulation theorem
- provides: Commutativity condition; Transcript-based proving complexity
- requires: Common Reference String; Dependency function; Leakage descriptor
- uses: Contract multiplexing; Deterministic transition function Δ; Distributed Ledger; Leakage function Λ; Ledger chain-data sub-contract; Non-interactive zero-knowledge proof; Public and local private state split; State oracle; State oracle transcripts; Unconfirmed transaction projection

## Keyed MAC  [concept_mac]  (primitive; 6 papers)
Onion franking uses a MAC over commitment and context values to authenticate messages for reports. Its unforgeability supports report authenticity; MAC.Sign is modeled as a PRF for the accountability bound.
Papers: 2002_back_hashcash, 2020_alwen_mls_insider, 2021_duguey_thesis, 2022_cong_key_lattice, 2023_eskandarian_abusereporting, 2024_gregoire_onionfranking
- provides: Hashcash-cookies; Unforgeability advantage bound

## Statistically-hiding commitment scheme  [concept_commitment_scheme]  (primitive; 6 papers)
A trapdoor-based scheme commits to an input while computational hiding prevents learning it without the trapdoor and computational binding makes it infeasible to open one commitment to distinct inputs. Trapdoors come from a specified generator, which need not sample uniformly.
Papers: 2014_bensasson_zerocash, 2016_hopwood_zcash_protocol_spec, 2017_shirazi_multiparty, 2022_shirali_dcnetsurvey, 2022_tzialla_transparencydictionaries, 2024_gregoire_onionfranking
- provides: Unforgeability advantage bound
- uses: Dual Mode DCN

## Unknown Key-Share Attack  [concept_unknown_key_share_attack]  (attack; 6 papers)
If the peer-to-peer key-sharing channel permits an unknown key-share attack, Eve can forward Alice's session keys to Bob, who may believe Alice initiated the session with him; the Megolm session inherits the channel vulnerability.
Papers: 2014_frosch_textsecure_analysis, 2016_matrix_megolm_spec, 2017_rosler_more_is_less, 2021_hashimoto_pq_x3dh_deniable, 2023_cremers_keeping_up_kems, 2026_bao_x3dh_tight
- attacks: Signal Protocol
- instance_of: Unknown key-share scenario

## ProVerif  [concept_proverif]  (primitive; 5 papers)
The authors use ProVerif for automated symbolic analysis of unbounded DR ratchets, state compromises, out-of-order handling, and header encryption. It automatically found the specification attack and guided discovery of implementation attacks.
Papers: 2015_decouchant_collusions, 2023_cremers_keeping_up_kems, 2024_bhargavan_pqxdh, 2025_wallez_thesis, 2026_cheval_dr_automated
- assumes: Dolev-Yao attacker
- attacks: None chain key attack
- compares_with: Complementary verification tools; DY∗ custom cryptography limitation; Within-step attacker interleaving limit
- measures: Public key confusion attack
- proves: Privacy property P3; Unbounded DR security proof
- uses: Idealized symmetric encryption

## Groth16  [concept_groth16]  (protocol; 5 papers)
The second recursive proof layer compresses a deVirgo proof into a constant-size proof that is fast for an EVM smart contract to verify; it is unsuitable for proving the full large zkBridge circuit directly.
Papers: 2016_hopwood_zcash_protocol_spec, 2022_taheri_waku_rln_relay, 2022_xie_zkbridge, 2026_babbush_ec_crypto_quantum, iog_zswap_zk_snark_based_non_interactive_multi_asset_swaps
- compares_with: BCTV14
- implements: Recursive verification; Sapling
- instance_of: zk-SNARK
- measures: Groth16 proof size
- proves: Circuit resource-count claims; Low-gate circuit variant; Low-qubit circuit variant
- uses: BLS12-381

## Proxy Re-Encryption (PRE)  [concept_proxy_re_encryption]  (primitive; 4 papers)
PRE lets a broker transform ciphertext for authorized subscribers without decrypting the payload or receiving decryption keys. A compromised broker with all re-encryption keys and observed communications can learn publisher–subscriber authorization relationships, but the paper claims payload confidentiality remains.
Papers: 2017_polyakov_fast, 2022_jin_secure, 2023_abdennebi_latticebased, 2023_abdennebi_latticepubsub
- instance_of: Unidirectional delegation
- leaks: Broker authorization-relationship leakage; PRE policy-authority exposure
- provides: Payload confidentiality under broker compromise; Publish/Subscribe
- requires: Per-subscriber PRE processing
- uses: Re-encryption key

## Unobservability  [concept_unobservability]  (property; 5 papers)
The paper treats unobservability as the strongest eavesdropper-facing relation and says its scenario relation places no restriction on matrix pairs; against malicious destinations it is inapplicable because destinations observe received traffic.
Papers: 2010_pfitzmann_terminology, 2013_gelernter_limits_provable_anonymity, 2015_barroso_adtn, 2018_recabarren_tithonus, 2022_shirali_dcnetsurvey
- extends: Undetectability
- improves_on: Sender anonymity
- requires: Anonymity

## Key derivation function (KDF)  [concept_kdf]  (primitive; 6 papers)
Derives an output string of a specified bit length from keying material, with optional salt and context. Outfox derives separate header and payload keys from each KEM shared key.
Papers: 2012_libert_anonymousbe, 2016_signal_double_ratchet_spec, 2024_rial_outfox, 2025_hashimoto_bundled_ake, 2025_wallez_treekem_verified, 2026_jarecki_x3dh_sas
- requires: IND-CCA security

## Gap Diffie–Hellman  [concept_gap_diffie_hellman]  (primitive; 6 papers)
GDH is the classical group assumption used for HybridOR channel security or ring-LWE security alternatives and for resistance to node impersonation. The chunk defines it with a DDH oracle in a prime-order group.
Papers: 2015_ghosh_pq_onion, 2016_cohngordon_signal, 2020_kreuter_anontokens, 2023_matrix_core_formal, 2024_fiedler_pqxdh_analysis, 2026_herouard_squirrel_ratchet
- proves: Inductive secrecy proof
- requires: Decision Diffie-Hellman

## TARANET  [concept_taranet]  (protocol; 2 papers)
A network-layer anonymity protocol that mixes setup messages and uses end-to-end traffic shaping with packet splitting during data transmission. Its prototype forwards over 50 Gbps on commodity hardware.
Papers: 2018_chen_taranet, 2020_kuhn_breaking
- assumes: Global active adversary
- compares_with: Tor
- measures: Prototype throughput
- proves: Ideal onion routing properties
- provides: Anonymity-set improvement; Non-collaborative AS relationship-set size; Payload integrity; Relationship anonymity; Replay protection; Shared flowlet keys
- requires: Data packet processing requirements; Link padding and encryption
- uses: Constant-rate link shaping; End-to-end payload encryption; End-to-end traffic shaping; Fixed-size onion packets; Flowlet; Onion-Security; Packet splitting; Packet-carried forwarding state; Path retrieval options; Per-packet expiration

## Blind Signature  [concept_blind_signature]  (primitive; 6 papers)
A privacy-preserving authentication mechanism for obtaining a signature on hidden data; the chunk cites it as an established primitive and describes a framework that uses committed messages and zero-knowledge proofs.
Papers: 2018_liu_keyinsulatedstealth, 2021_agrawal_lattice_blind_sig, 2021_martiny_sealed_sender, 2023_beullens_lattice_blind_sig, 2023_lai_commit_transferrable_sig, 2024_argo_pq_signatures_privacy
- compares_with: Derived-key privacy
- provides: Honest-signer blindness; One-more unforgeability
- uses: Blind signature flow; Commit-Transferrable Signature (CTS)

## Coconut  [concept_coconut]  (protocol; 1 papers)
Threshold issuance credentials use blind signing by authorities, aggregation of partial credentials, and randomized credential proofs. The chunk states security properties under XDH and describes an Ethereum tumbler application.
Papers: 2019_sonnino_coconut
- assumes: LRSW assumption; XDH assumption
- instance_of: Selective disclosure credentials
- measures: Global aggregation latency; Verification latency
- proves: Threshold credential security theorem; Threshold unforgeability
- provides: Asynchronous issuance; Blind issuance; Constant-size credentials; Issuance communication complexity; Multi-attribute credential; Publicly verifiable showing; Show and verification complexity; Unlinkable showings
- requires: Distributed key generation fault bound; Ethereum block gas limit; Honest majority threshold
- uses: Credential re-randomization; El Gamal; One-time verification key aggregation; Pedersen commitment; Pointcheval-Sanders signature; Private attribute commitment; Shamir secret sharing; Threshold issuance; Zero-Knowledge Proof

## Private Information Retrieval  [concept_pir]  (primitive; 5 papers)
CPIR-based systems can store each round's messages and let clients poll missed rounds after reconnecting without additional information leakage, at the cost of server storage and computation. The chunk says CPIR-family proposals are computationally expensive and incur prohibitively high delivery latency.
Papers: 2020_kuhn_sokperformance, 2023_patel_keywordpirsparse, 2023_sasy_sokmetadata, 2026_ramesh_sensing, 2026_ravi_remise

## HQC  [concept_hqc]  (primitive; 4 papers)
A code-based cryptosystem used as RHQC's public key encryption primitive. Its default parameters are described as IND-CPA secure under 2-DQCSD-P and 3-DQCSD-PT hardness assumptions.
Papers: 2022_xagawa_anonymitykems, 2025_alagic_best_of_both_kems, 2025_hqc_specification, 2025_juaneda_rhqc
- assumes: Fixed-weight randomness
- contradicts: Ciphertext collision resistance
- leaks: HQC ciphertext parity leakage
- measures: AVX2 implementation performance; Reference implementation performance
- proves: IND-CCA2 security; IND-CPA security
- provides: Ciphertext second preimage resistance (C2PRI); Constant-time implementation; HQC key and ciphertext sizes; HQC parameter sets
- requires: HQC correctness condition
- uses: Fujisaki–Okamoto transform; Reed-Muller code; Systematic Reed-Solomon code

## Brahms  [concept_brahms]  (protocol; 2 papers)
A tolerance-based peer-sampling protocol that limits membership messages processed per round and uses min-wise independent samplers to extract uniform samples from a potentially biased stream; the text says it remains highly vulnerable to Byzantine attack even with a small Byzantine fraction.
Papers: 2023_auvolat_basalt, 2026_mukam_byzantineresilient
- assumes: Brahms message-rate limit assumption
- measures: Brahms result at 18% malicious nodes
- proves: Brahms uniform-sampling guarantee
- uses: Brahms excess-push blocking; Brahms history sampling; Brahms push-pull parameters; Min-wise independent permutations; Min-wise sampling

## Onion Franking  [concept_onion_franking]  (protocol; 1 papers)
A mechanism for metadata-hiding messaging systems based on onion encryption to support lightweight, verifiable abuse reports while retaining relevant sender and receiver anonymity, including for reported messages. The paper claims its construction is most efficient in computation and communication for each targeted security level, but gives no headline numerical comparison in this chunk.
Papers: 2024_gregoire_onionfranking
- assumes: Pseudorandom function; Random oracle simulation
- compares_with: Optimized scheme comparison with Hecate
- extends: End-to-end encryption
- implements: Layered mixing
- improves_on: Message Franking
- instance_of: Metadata Privacy
- measures: Communication overhead formulas; Measured optimized timings; Measured zero-knowledge timings; Per-message communication savings
- proves: Accountability advantage bound; Unforgeability advantage bound
- provides: Abuse reporting; Anonymity; Anonymous reporting; Post-report confidentiality scope
- requires: Context must hide sender identity; Onion Encryption
- uses: Keyed MAC; Onion Encryption; Preprocessed Send values; Seed-based mask shrinking; Statistically-hiding commitment scheme; Zero-Knowledge Proof

## AetherWeave  [concept_aetherweave]  (protocol; 1 papers)
AetherWeave uses stake-backed peer discovery, peer-table sampling, attack-detection flags, and slashing. This chunk proves partition-resistance and privacy claims and describes a prototype.
Papers: 2026_alpturer_aetherweave
- assumes: Adversarial stake fraction; Known-address connectivity assumption; Mean-field approximation; Network adversary
- contradicts: Partitioning limitation
- defends_against: Eclipse Attack; Sybil Attack
- measures: Prysm prototype
- proves: Connection privacy result; Partition resistance result; Record visibility convergence; Table quality equilibria; Visibility reproduction threshold
- provides: Authenticated private channels; Connectivity or detection guarantee; On-chain interaction scope; Stake and network identity unlinkability
- requires: Address churn and address supply; Per-round request limit
- uses: Authenticated peer records; Global per-round request quota; Gossip and private peer tables; Low record count eclipse signal; Private-table overlay sampling; Record freshness and table cap; Seed-based record filtering; Stake-backed participation; Threshold parameter choice

## UnifOMR  [concept_unifomr]  (protocol; 1 papers)
Single-server OMR using RLWE-based additively homomorphic encryption and batch PIR. At N=2^19 messages of 612 bytes, it takes about 25 seconds, uses 4 MB communication, and has a 31 MB detection key; it requires two rounds and a digest linear in N.
Papers: 2026_fisch_unifomr
- assumes: Brakerski/Fan-Vercauteren (BFV); RLWE assumption
- compares_with: ECDH; Private Information Retrieval; SophOMR
- extends: UnifOMD
- implements: Client-aided retrieval
- improves_on: Client communication and computation savings; Fully homomorphic encryption (FHE)
- instance_of: Oblivious Message Retrieval
- measures: Batch PIR runtime share; Measured speedup range
- provides: Linear digest size; Strong detection-key-unlinkability
- requires: Security assumptions; Two rounds of interaction
- uses: Additively Homomorphic Encryption (AHE); Batch PIR; Brakerski/Fan-Vercauteren (BFV); Private Information Retrieval; RLWE-based PKE for clues; SIMD packing

## Pepper  [concept_pepper]  (protocol; 1 papers)
A computational-cryptography anonymous broadcast protocol built on a two-server DC-net. It supports anonymous registration, batch writes, and sender anonymity against a global adversary when at least one aggregation server is honest.
Papers: 2026_li_pepper
- assumes: Anytrust assumption; Cryptographic assumptions; Global Network Adversary
- contradicts: Denial of service attack; Intersection attack
- defends_against: Disruption attack; Traffic correlation attack
- implements: Anonymous channel registration
- measures: Implementation size; Pepper per-epoch cost; Registration audit latency
- provides: Anonymity Set; Batch messaging; Metadata Privacy; Public bulletin; Registration sender anonymity; Server deviation recovery
- uses: Aggregation server pair; Cohort selection statistics; Cover Traffic; DC-net; Distributed Multi-Point Function (DMPF); Distributed Point Function; Schnorr Proof over Secret Shares (SPoSS); TLS; Two-server cohort; Verifiable DMPF (VDMPF)

## DDH assumption  [concept_ddh_assumption]  (assumption; 6 papers)
The seed-homomorphic PRG can be built from DDH using random public generators in a prime-order group where DDH is hard; an elliptic-curve group is an example.
Papers: 2012_libert_anonymousbe, 2015_corrigangibbs_riposte, 2019_sonnino_coconut, 2024_gregoire_onionfranking, 2025_chu_signalingmalicious, 2026_qian_silentpayments

## Plumtree  [concept_plumtree]  (protocol; 6 papers)
Uses duplicate detection and link deactivation to form a spanning tree; inactive links carry lazy-push message-ID announcements for recovery, at the cost of latency-sensitive unnecessary recoveries or ongoing overhead.
Papers: 2012_matos_brisa_combining, 2017_ssb_protocol_guide, 2018_meiklejohn_partisan, 2019_banno_interworking_layer, 2020_savolainen_streamr_network, 2022_manuceau_ipfs_pubsub_ca
- compares_with: BRISA tree and DAG; Control message cost; Network-partition tolerance tradeoff
- implements: Transitive Delivery
- uses: Gossip protocols

## End-to-end encryption  [concept_end_to_end_encryption]  (primitive; 6 papers)
In the studied messengers, E2EE leaves server infrastructure unaware of non-compliant message contents, such as reactions to nonexistent messages, and prevents server-side message validation. It requires rigorous validation by receiving clients.
Papers: 2014_coull_imessage_privacy, 2022_eskandarian_clarion, 2024_gegenhuber_careless_whisper, 2025_jiang_fpgaomr, 2026_firmansyah_decentralized_messaging_metadata, 2026_gegenhuber_whatsapp_enumeration
- contradicts: E2EE social-graph privacy limit
- leaks: Metadata Privacy; Session recovered metadata records
- requires: Server visibility limits

## ASPE  [concept_aspe]  (primitive; 4 papers)
An encryption scheme that preserves scalar-product computation and distance differences, not actual distances. It uses subscriber key M and publisher key M⁻¹; matching yields D₂ = D₁q for positive random scalar q.
Papers: 2014_onica_efficient, 2015_onica_efficient, 2016_onica_confidentialitypreserving, 2017_barazzutti_efficient
- compares_with: ASPE security evaluation
- defends_against: Distance-preserving encryption KPA risk
- measures: ASPE matching complexity
- provides: Encrypted distance-difference matching; Stock quote notification use case
- requires: ASPE shared private-key distribution; Encrypted subscription memory

## Equihash  [concept_equihash]  (protocol; 2 papers)
An asymmetric proof of work based on the generalized birthday problem and Wagner’s algorithm, designed to require substantial prover memory while allowing fast, low-memory verification.
Papers: 2016_biryukov_equihash, 2022_park_superlinearity
- assumes: Communication-limited parallelism
- compares_with: BitTorrent
- improves_on: Memory-hard computing
- instance_of: Asymmetric proof of work; Impossibility result; Proof of Work
- measures: 250 MB memory reduction penalty; 700 MB reference configuration; Equihash implementation benchmark; Memoryless algorithm cost; Small solution-count deviation
- proves: Algorithm-bound tradeoff; Bandwidth advantage bound; Parallel time bound; Standard tradeoff
- provides: Asymmetric proof of work; Equihash parameterized specification; Proof-of-work design requirements
- requires: Memory bandwidth
- uses: Algorithm binding; Difficulty filter; Generalized birthday problem; Wagner’s algorithm

## Robustness  [concept_robustness]  (property; 4 papers)
Robustness for encryption schemes concerns difficulty producing ciphertext valid for different key pairs; the chunk reviews weak and strong forms and stronger variants allowing secret-key queries or adversarial key generation.
Papers: 2020_abraham_blinder, 2022_grubbs_anonrobustpq, 2022_xagawa_anonymitykems, 2023_cremers_keeping_up_kems
- extends: Complete robustness

## XSalsa20/Poly1305  [concept_xsalsa20_poly1305]  (protocol; 3 papers)
A widely used AEAD combining the XSalsa20 stream cipher and Poly1305 MAC, noted for speed, constant-time software implementation ease, and security properties. It is vulnerable to the discussed key multi-collision attack.
Papers: 2021_len_partitioningoracle, 2023_paterson_threema, 2024_jaeger_keybase_signcryption
- implements: BoxMessage
- uses: Key multi-collisions; Poly1305; Zeros-check transform

## DoublePIR  [concept_doublepir]  (protocol; 4 papers)
Recursively applies SimplePIR twice to reduce hint size to roughly n² independent of database size, while reporting 7.4 GB/s server throughput; its per-query communication is O(√N).
Papers: 2022_henzinger_simplepir, 2023_li_hintlesspir, 2024_menon_ypir, 2025_mahdavi_inspire
- defends_against: Long-term PIR state risk
- measures: Batched throughput; DoublePIR daily-update cost; DoublePIR query costs; DoublePIR weekly cost; PIR throughput results; Per-query cost
- provides: DoublePIR hint size
- requires: DoublePIR hint; Multiple SCT database copies
- uses: SimplePIR

## El Gamal  [concept_el_gamal]  (protocol; 5 papers)
Coconut uses El-Gamal encryption to let users submit private attributes for blind signing. The user decrypts each authority's encrypted partial signature using its private key.
Papers: 2001_bellare_keyprivacy, 2018_bhargavan_treekem, 2018_davidson_privacypass, 2019_sonnino_coconut, 2022_thambipillai_streamr_multicast_encryption
- assumes: DDH assumption
- proves: El Gamal anonymity bound
- provides: IK-CPA
- requires: Decision Diffie-Hellman
- uses: Curve25519; PBKDF2

## Searchable Encryption  [concept_searchable_encryption]  (primitive; 4 papers)
ABKS-UR encrypts topics and subscription keywords, generates trapdoors, matches encrypted indexes at the broker, and supports subscriber revocation. Its modified version gives correctness when attributes satisfy the access policy and keywords match.
Papers: 2011_shikfa_brokerbased, 2022_fleischhacker_compressencrypted, 2022_klingler_confidentialite, 2024_chou_bots_groupchats
- proves: Modified ABKS-UR correctness; Semantic security of keywords
- provides: Selective access lacks forward secrecy; Subscriber revocation; Subscription confidentiality
- uses: Sparse ciphertext compression

## ElGamal encryption  [concept_elgamal_encryption]  (primitive; 6 papers)
Verdict implements verifiable DC-net constructions using ElGamal encryption in conventional integer groups and elliptic-curve groups. These constructions offer an order of magnitude lower computational cost than the pairing approach.
Papers: 2013_corrigangibbs_verdict, 2014_chase_algebraicmacs, 2021_behl_trusted_notifications, 2022_bienstock_dr_uc, 2026_shen_trustmix, iog_syra_sybil_resilient_anonymous_signatures_with_applications
- measures: ElGamal computation cost
- requires: Intermediate secret hidden; Type-III asymmetric bilinear groups

## Key Indistinguishability  [concept_key_indistinguishability]  (property; 5 papers)
The analyzed goal is that no efficient adversary wins the multi-stage key-indistinguishability game for the two-party protocol with non-negligible probability, subject to freshness conditions.
Papers: 2016_cohngordon_signal, 2018_poettering_asynchronous_rke, 2024_fiedler_pqxdh_analysis, 2025_collins_leakage_rke, 2026_auerbach_anonauthkem
- proves: Classic key-indistinguishability bound
- requires: Bounded leakage; Freshness and cleanness conditions
- uses: Test query

## Saber  [concept_saber]  (system; 4 papers)
Saber’s transform derives k̂,r from G(F(pk),m), encrypts m with randomness r, and derives the key as F(k̂,F(c)); the nested ciphertext hash complicates QROM security and anonymity proofs.
Papers: 2022_grubbs_anonrobustpq, 2022_maram_pq_anonymity_kyber, 2022_xagawa_anonymitykems, 2026_basso_kopis
- assumes: Module Learning With Rounding
- compares_with: Quantum random oracle model
- instance_of: QROM extra-hash proof barrier
- proves: Decryption-failure attack cost
- provides: Robustness
- requires: Two-decapsulation-oracle simulation obstacle
- uses: Nested ciphertext hash

## Collision-resistant hash function  [concept_collision_resistant_hash]  (primitive; 6 papers)
For label-augmented security definitions, the chunk says the hash H must be collision-resistant rather than only target collision-resistant. The KD* construction also specifies a universal one-way hash function for its base setup.
Papers: 2012_libert_anonymousbe, 2014_bensasson_zerocash, 2021_hu_merkle2, 2022_grubbs_anonrobustpq, 2023_jakkamsetti_scalablesignaling, 2024_hansen_ocash
- requires: Guarantee 1

## HyParView  [concept_hyparview]  (protocol; 5 papers)
A hybrid gossip membership protocol using partial views for scalable global connectivity; failures may break connectivity or increase route length, so views are maintained by different strategies.
Papers: 2012_matos_brisa_combining, 2013_rene_erreichen, 2016_chen_omen, 2018_meiklejohn_partisan, 2022_manuceau_ipfs_pubsub_ca
- compares_with: Backup sets
- implements: Active and passive views
- instance_of: Peer sampling service
- uses: Partial Views; View expansion factor

## Argon2i  [concept_argon2i]  (protocol; 2 papers)
A data-independent memory-hard password hashing function evaluated in single-pass and multipass configurations. The chunk gives a sequential time-space lower bound and reports that its one-pass variant requires roughly 1.5 MiB at the stated authentication rate.
Papers: 2016_biryukov_argon2, 2016_boneh_balloon
- attacks: Multi-pass Argon2i space attack; Single-pass Argon2i space attack
- compares_with: Balloon Hashing; Balloon throughput comparison
- defends_against: Argon2i memory-leak resistance
- implements: Data-independent memory access
- leaks: Access-pattern precomputation attack
- measures: Argon2i speed; Authentication throughput target
- proves: Argon2i single-pass lower bound
- provides: Three-pass Argon2i tradeoff; Variant selection by side-channel risk
- uses: Argon2i block size

## scrypt  [concept_scrypt]  (primitive; 4 papers)
The paper analyzes scrypt’s ROMix core: it computes an n-step hash chain, then n further hash outputs selected using the preceding state modulo n. It is used in cryptocurrency proof-of-work schemes, including Litecoin and Dogecoin.
Papers: 2016_biryukov_equihash, 2016_boneh_balloon, 2017_alwen_scrypt, 2021_tron_book_of_swarm
- compares_with: Balloon Hashing; Proof of Work
- implements: Scrypt hash chain; Scrypt indexed phase; Session key
- instance_of: Memory-hard function (MHF); Parallel random-oracle model
- leaks: Cache-timing attack
- measures: Cumulative memory complexity (ccmem)
- part_of: Balloon then scrypt composition
- proves: Sequential memory-hardness definition; scrypt memory hardness theorem
- uses: Random oracle simulation

## VCube-PS  [concept_vcube_ps]  (system; 2 papers)
A topic-based publish/subscribe system over a virtual hypercube-like VCube topology. It broadcasts membership information and publications over dynamically built spanning trees rooted at each publisher, and enforces causal delivery per topic.
Papers: 2017_araujo_vcubeps, 2019_araujo_communication_causal
- assumes: Asynchronous network; Failure-free reliable model; System model assumptions
- compares_with: SRPT
- implements: Forwarding after unsubscribe; Membership broadcast; Per-publisher spanning trees
- instance_of: Topic-Based Pub/Sub; Topic-Connected Overlay
- measures: Performance claims
- provides: Causal Ordering; Causal broadcast per topic
- requires: MAX_TOPICS; Maximum topics parameter; System size
- uses: Dynamic per-source topic trees; Message fields and types; Message types; Topic subscriber tree; VCube; VCube topology

## Conflict-Free Replicated Data Type  [concept_conflict_free_replicated_data_type]  (primitive; 4 papers)
Replicated data types let replicas update and answer queries locally, including during partitions, while asynchronous update propagation supports convergence. Concurrent semantics are built into the data type, including for non-commutative operations.
Papers: 2018_meiklejohn_partisan, 2021_berty_wesh_protocol, 2022_guidec_supportingconflict, 2024_almeida_approachesconflict
- provides: Delta-state CRDTs; Local availability and response time; Operation-based CRDTs; State-based CRDTs; Strong Eventual Consistency (SEC)
- uses: Lamport clock ordering; Operation-based CRDTs; State-based CRDTs

## Chained CmPKE  [concept_chained_cmpke]  (protocol; 2 papers)
The proposed CGKA lets the delivery service sanitize commits by sending member i only decryptable ciphertext ct_i. Upload cost is O(N), download O(1), and total commit bandwidth O(N); experiments report computation and processing below 100 ms even for N=2^10.
Papers: 2021_hashimoto_chained_cmpke, 2022_hashimoto_mls_metadata
- compares_with: TreeKEM
- implements: Per-recipient commit sanitization
- improves_on: Chained mKEM cost; TreeKEM
- measures: CmPKE computation timings; Commit computation runtime; Commit upload bandwidth; Upload comparison threshold; Welcome and join message cost
- motivates: Signal Protocol
- proves: Chained CmPKE security proof; Extended UC security model
- provides: O(N) upload and O(1) download; One keypair per user
- requires: Delivery-service commit editing; sEUF-CMA signature security
- uses: CmPKE; Multi-Recipient PKE; Multi-recipient public-key encryption (MRPKE); Selective (designated) downloading

## Trusted Execution Environment  [concept_trusted_execution_environment]  (primitive; 5 papers)
A TEE can perform collision tests while keeping a secret key and state in protected memory. The paper cites SGX enclaves with about 128 MB protected memory and substantial paging overhead; VSM's trusted component needs only O(1) private memory.
Papers: 2021_madathil_privatesignaling, 2022_hagen_contactdiscovery, 2022_li_sok, 2023_jakkamsetti_scalablesignaling, 2026_zarchy_selfmix
- uses: TC misuse detection

## OPRF  [concept_oprf]  (protocol; 2 papers)
The protocol computes a PRF output while hiding the client's private input from the server, even against unbounded computation; the server also learns neither the output nor the client learns its private key.
Papers: 2023_rfc9497_oprf, 2024_rfc9578_privacypass_issuance
- assumes: One-More Gap CDH assumption
- measures: Batch test sizes
- provides: Input secrecy and unlinkability; Output size; Server output secrecy
- requires: Server key derivation
- uses: Serialized element size

## Groove  [concept_groove]  (protocol; 5 papers)
Groove supports low-latency, high-throughput, horizontally scalable messaging but not full asynchrony; it allows temporary disconnection for a constant number of rounds, after which users can no longer receive messages.
Papers: 2023_sasy_sokmetadata, 2024_diaz_reliability, 2025_kaviani_myco, 2026_basso_kopis, 2026_davitt_mixnetusability
- assumes: Differential Privacy
- compares_with: A posteriori reliability estimation; Selected mean delay levels
- extends: Karaoke; Mixnet
- instance_of: Differential Privacy
- measures: Latency
- provides: Anonymity Set; Metadata Privacy
- uses: Groove oblivious delegation

## Decisional Diffie–Hellman assumption  [concept_decisional_diffie_hellman_assumption]  (assumption; 6 papers)
The unlinkability proof assumes DDH; distinguishing a hybrid ciphertext containing a Diffie–Hellman element from one containing a random group element would break DDH.
Papers: 2009_danezis_sphinx, 2018_ando_practical_onion_routing, 2021_vatandas_signal_deniability, 2023_kovacs_umbra_anonymity, 2024_len_elektra, 2026_shen_trustmix
- assumes: Rotatable Zero Knowledge Set (RZKS)

## Ciphertext-Policy Attribute-Based Encryption  [concept_ciphertext_policy_attribute_based_encryption]  (primitive; 5 papers)
Encrypts data under an access structure represented as a tree; user attributes determine whether decryption can reconstruct the plaintext. The paper uses it for policy-based access control in IIoT.
Papers: 2012_pal_p3s, 2014_yang_privacypreserving, 2014_yang_privatepubsubcloud, 2023_abdennebi_latticebased, 2025_li_dpsiiot
- compares_with: Key-Policy Attribute-Based Encryption (KP-ABE)
- provides: Data confidentiality
- requires: Publisher
- uses: Access policy tree

## AODV  [concept_aodv]  (protocol; 5 papers)
Ad hoc On-Demand Distance Vector is used as a comparison for fully mobile communication. It discovers unicast routes on demand, with hello messages for neighbor/link status and broadcast RREQ for unknown destinations.
Papers: 2012_schnitzer_content_routing, 2016_royer_content, 2016_royer_routagebase, 2021_amozarrain_fully, 2024_chovet_performancecomparison
- compares_with: MFT-PubSub
- instance_of: Mesh network
- measures: AODV versus ideal routing
- motivates: Broadcast Storm
- uses: IP network layer; Publish/Subscribe

## Verifiable shuffle  [concept_verifiable_shuffle]  (primitive; 4 papers)
Servers shuffle N client-submitted pseudonym slot keys so their public order is permuted and no participant learns which other client submitted which key. Dissent’s verifiable shuffle also broadcasts accusations and dominates disruption-identification cost.
Papers: 2012_wolinsky_dissentnumbers, 2013_corrigangibbs_verdict, 2016_kwon_riffle, 2022_eskandarian_clarion
- compares_with: Evaluation method
- defends_against: Shuffle duplication attack
- implements: Neff's verifiable shuffle
- measures: Dissent accusation shuffle time; Verifiable shuffle cost
- uses: Chaum-Pedersen proofs; ElGamal encryption

## Proofs of Space (PoS)  [concept_proofs_of_space]  (protocol; 1 papers)
A prover initializes by storing an N-sized file and later proves access to it; the verifier should use at most polylogarithmic work and communication in N and polynomial resources in security parameter γ.
Papers: 2015_dziembowski_proofsofspace
- assumes: Random oracle simulation
- compares_with: PoS and secure-erasure distinction
- defends_against: Sybil Attack
- improves_on: Proof of Work
- part_of: Initialization and execution phases
- provides: Public protocol values
- requires: Adversary output-set assumption; Statistical security parameter γ; Storage bound 2N
- uses: Execution challenges; Graph pebbling; Graph-derived values; Hash tree; Merkle Hash Tree; Random consistency checks

## Adaptive diffusion  [concept_adaptive_diffusion]  (protocol; 2 papers)
The paper adapts an earlier adaptive diffusion protocol into a realistic protocol for current peer-to-peer networks, using distance-distribution-based virtual-source probabilities and a reduced-information attacker model.
Papers: 2015_fanti_hidingrumor, 2021_modinger_statistical
- extends: Grid adaptive diffusion
- implements: Pólya urn adaptive implementation; Tree Protocol
- leaks: Control packet source leakage; Hop-count distance leak
- proves: Adaptive diffusion spy detection; Adaptive estimate-distance bound
- provides: Infection and anonymity threshold; Jordan centre; Runtime guarantee claim; Snapshot game dominance
- uses: Privacy-friendly equation solution; Virtual source selection; η-neighbour selection

## Hidden Services  [concept_hidden_service]  (mechanism; 4 papers)
Each user identity is represented by a hidden service as its connection point. While online, the user publishes the service corresponding to the onion hostname in the contact ID and accepts bidirectionally anonymous connections.
Papers: 2015_unger_sok_securemessaging, 2016_ncc_ricochet_audit, 2016_sanatinia_honeyonions, 2022_ricochet_refresh_design
- implements: Pond; Ricochet
- provides: Contact ID; Forward Secrecy
- uses: Hidden Service Directory (HSDir); Rendezvous Point

## POSEIDON  [concept_poseidon]  (system; 4 papers)
Poseidon hashes the identity secret, identity commitment, external and internal nullifiers, and polynomial coefficient; the canonical implementation lists parameters for 1–8 inputs, with RF=8 and RP from 56 to 64.
Papers: 2016_hakiri_datacentric, 2022_vac_rln_v1_spec, 2024_midnight_zswap_spec, iog_zswap_zk_snark_based_non_interactive_multi_asset_swaps
- implements: Tunnel endpoint programming
- part_of: POSEIDON control-plane agent
- provides: Brokerless architecture
- uses: Monitoring message; OpenFlow; Routing agent; Topic filtering; Topic-Based Pub/Sub

## Sapling  [concept_sapling]  (protocol; 3 papers)
Sapling derives spending, proof authorization, and outgoing viewing keys from a random spending key using PRFexpand; it supports diversified payment addresses sharing viewing keys. Address-generation choices can reveal information through diversifiers.
Papers: 2016_hopwood_zcash_protocol_spec, 2022_namada_masp_spec, iog_zswap_zk_snark_based_non_interactive_multi_asset_swaps
- leaks: Sapling vanity diversifier leak
- provides: Sapling Faerie Gold protection; Sapling diversifier index recommendation
- uses: Outgoing ciphertexts and ock; PRFnr output uniformity; Pedersen chunks per segment; Randomness beacon; RedDSA; RedJubjub; Sapling Merkle depth; Sapling Pedersen commitments; Zero-Knowledge Proof

## VOPRF construction  [concept_voprf]  (primitive; 2 papers)
A verifiable OPRF variant: the client completes only after checking correctness against a server key commitment. Its pseudorandomness, input secrecy, and verifiability rely on One-More Gap CDH in the prime-order group.
Papers: 2018_davidson_privacypass, 2023_rfc9497_oprf
- assumes: One-More Gap CDH assumption
- extends: OPRF
- measures: Batch test sizes
- provides: Output size; VOPRF batch one vector one; VOPRF batch one vector two; VOPRF batch two vector; VOPRF outputs; VOPRF proof values
- requires: Key commitment for verifiability; Server key derivation
- uses: Serialized element size; Serialized scalar size; VOPRF blind values; VOPRF key setup

## Fiat–Shamir transform  [concept_fiat_shamir_transform]  (primitive; 5 papers)
Removes verifier interaction in a Sigma protocol by deriving the challenge as h(a,x) from commitment a and public statement x. Its signature security was proven in the ROM using the forking lemma; zero knowledge additionally needs oracle programmability.
Papers: 2019_tyagi_messagefranking, 2021_duguey_thesis, 2023_tessaro_bbs, 2024_gregoire_onionfranking, 2026_draft_act
- assumes: Random oracle model
- provides: Oracle programmability
- requires: Oracle programmability
- uses: Forking lemma; Sigma protocol

## QUIC  [concept_quic]  (protocol; 6 papers)
QUIC uses the TLS-family ρ-chain for key updates and is affected by the discussed TMTO and collision attacks; the chunk recommends replacing key updates with ephemeral key exchange.
Papers: 2020_jefferys_session, 2021_rohrer_kadcast_ng, 2022_albrecht_telegram, 2024_mattsson_symmetric_ratchets, 2025_farooq_preamble, 2025_wallez_thesis
- improves_on: No transport prioritization; Polling overhead
- uses: ρ-chain

## Lightning Network (LN)  [concept_lightning_network]  (system; 2 papers)
Bitcoin layer-2 payment network with source-routed payments and centralized routing paths: a few high-centrality nodes can intercept a disproportionate share of transactions. Its latest evaluated snapshot has median anonymity entropy of zero, and 1% influential adversaries can fully deanonymize about 50% of transactions.
Papers: 2021_kappos_lnprivacy, 2023_sharma_p2panonymity
- instance_of: Payment Channel Network (PCN)
- provides: Centrality concentration; Lightning liveness information; Successor information leakage
- requires: Known LN topology
- uses: BitTorrent; Hashed timelock contracts (HTLCs); Onion Routing

## Private signaling  [concept_private_signaling]  (protocol; 2 papers)
A sender posts a message location signal so only the intended recipient can identify it, without out-of-band communication or prior shared state. The goal is full recipient privacy with constant sender and recipient work.
Papers: 2021_madathil_privatesignaling, 2023_jakkamsetti_scalablesignaling
- extends: Multi-server extension
- implements: Encrypted linked-list storage
- improves_on: Prior server-work bound
- instance_of: Publish/Subscribe
- measures: Per-signal server cost; Retrieval server cost
- motivates: Constant sender and recipient work
- provides: Recipient anonymity; Recipient identity privacy; Retrieval unlinkability; Sender identity privacy; Total server-work bound
- requires: Public ledger
- uses: Encrypted retrieval request; Key-private PKE; Oblivious RAM; Trusted Execution Environment; Universal composability (UC) framework; Verification-key ORAM

## Module Learning With Errors  [concept_mlwe]  (assumption; 5 papers)
The post-quantum anonymity and IND-CCA results for Kyber rely on hardness of the module learning-with-error problem. The chunk gives no concrete hardness parameter or advantage bound.
Papers: 2022_maram_pq_anonymity_kyber, 2023_beullens_lattice_blind_sig, 2023_pu_fuzzystealthsigs, 2025_gunther_hybrid_obfuscated_kex, 2026_basso_kopis

## BIKE  [concept_bike]  (primitive; 3 papers)
BIKE is a binary linear QC-MDPC code-based KEM, initially designed for ephemeral keys and now claiming static-key support. Its FO-transformed PKE claims IND-CCA2 security if the PKE is δ-correct for δ ≤ 2^-λ.
Papers: 2022_xagawa_anonymitykems, 2025_alagic_best_of_both_kems, 2025_nist_ir8545_hqc
- assumes: IND-CPA from QCSD and QCCF
- instance_of: U⊥ and U̸⊥ KEM design
- provides: Ciphertext second preimage resistance (C2PRI)
- requires: δ-correctness requirement
- uses: BIKE QC-MDPC design; FO transform; Niederreiter-style encryption

## Tamarin  [concept_tamarin]  (system; 4 papers)
A symbolic cryptography protocol verifier that models participants with labeled multiset rewriting rules and machine-checks proofs; termination is not guaranteed because the underlying problem is undecidable.
Papers: 2023_beguinet_tamarin_pqsignal, 2023_cremers_keeping_up_kems, 2024_linker_imessage_pq3, 2025_wallez_thesis
- compares_with: DY∗ custom cryptography limitation; Within-step attacker interleaving limit
- measures: First symbolic proof result; Kyber-AKE; PQ-SPDM; TAMARIN measured results
- proves: Fine-grained secrecy and authentication properties
- uses: Dolev-Yao attacker; Nested-loop proof methodology

## K-Waay  [concept_k_waay]  (protocol; 2 papers)
A deniable X3DH-like protocol using FrodoKEX+ as a post-quantum split-KEM, PQ KEMs, and a signature scheme. The paper benchmarks its performance, sizes, and operational risks.
Papers: 2024_collins_k_waay, 2025_niot_sparrow_kem
- extends: X3DH
- improves_on: Ring signature limitations
- measures: Benchmark speedup; K-Waay speed result; Protocol data sizes
- requires: Asynchronous prekey setup; IND-1BatchCCA; UNF-1KCA
- uses: Frodo key exchange (FrodoKEX); FrodoKEX+; Pre-key bundles; Signed prekeys; Split-KEM; Three key sources

## Freenet  [concept_freenet]  (system; 5 papers)
Freenet is given as an example of a darknet using virtual overlays for content discovery and private communication. The text says darknet connections are restricted to users with real-world trust relationships.
Papers: 2003_goel_herbivore, 2012_mulamba_design, 2014_roos_measuring_freenet, 2015_roos_impossibility_self_stabilization, 2019_kuhn_privacynotions
- instance_of: Publish/Subscribe
- motivates: Anonymous file replication
- part_of: Darknet; Opennet
- provides: Private communication use case; Publisher and subscriber anonymity
- uses: Deterministic distance-directed routing; Freenet dynamic storage and routing

## Pseudorandom permutation  [concept_pseudorandom_permutation]  (primitive; 5 papers)
A keyed permutation family is indistinguishable from a random permutation to polynomial-time adversaries with adaptive access to the permutation and its inverse. The construction uses simultaneously pseudorandom permutations for multiple block lengths.
Papers: 2005_camenisch_onion_formal, 2018_giacon_kem_combiners, 2019_corrigangibbs_sublinear_pir, 2022_corrigangibbs_pirsublinearamortized, 2022_fleischhacker_compressencrypted
- implements: Blockcipher; PRP-based set membership test
- proves: PRP set inclusion probability
- provides: Puncturable pseudorandom set
- uses: Tagged encryption and PRP construction

## Disclosure Attack  [concept_disclosure_attack]  (attack; 5 papers)
A long-term observer can infer how frequently a sender communicates with a receiver and recover behavioral profiles when communications persist, despite high-latency anonymity preventing certainty about partners.
Papers: 2013_oya_sda_family, 2014_oya_real_world_sda, 2019_leibowitz_silentmixes, 2019_lu_survey, 2022_shirali_dcnetsurvey
- attacks: Communication relationship recovery
- compares_with: Intersection attack; Tor path-compromise attack metric
- defends_against: Dummy Traffic
- instance_of: Traffic Analysis
- leaks: Metadata Observation
- provides: Relationship-frequency inference

## DP5  [concept_dp5]  (protocol; 3 papers)
Dagstuhl Privacy Preserving Presence Protocol provides online presence and auxiliary data while keeping buddy lists private. Infrastructure servers require no long-term secrets and are designed for forward secrecy.
Papers: 2015_borisov_dp5, 2017_piotrowska_annotify, 2018_mp3_privatepresence
- provides: Anonymous-channel support; Auxiliary-data privacy; Directed friend registration; Offline, suspension, and revocation indistinguishability; Presence query; Privacy of presence; Social graph privacy; Unlinkability between epochs
- uses: Information-theoretic PIR; Long-term presence-key indirection; Private Information Retrieval

## MCMix  [concept_mcmix]  (system; 4 papers)
Anonymous messaging built from secure multiparty computation, with separate dialing and conversation operations. The chunk says it scales to hundreds of thousands of users and aims to hide communication metadata from a global adversary.
Papers: 2017_alexopoulos_mcmix, 2019_lu_asynchromix, 2022_eskandarian_clarion, 2023_sasy_sokmetadata
- compares_with: DC-net; Mixnet; Vuvuzela
- implements: Sharemind
- improves_on: Clarion
- measures: Hundreds-of-thousands scale
- provides: Metadata Privacy
- uses: Conversation functionality; Dialing functionality; Multiple-KGC identity-based key agreement; Secure Multi-Party Computation

## AMQP  [concept_amqp]  (protocol; 5 papers)
AMQP 0-9-1 is used for RabbitMQ experiments. The benchmark reports that RabbitMQ-AMQP failed after 500 client pairs in every VM configuration, attributed to heavier connection-management and channel-multiplexing overhead.
Papers: 2018_johnsen_publishsubscribe, 2018_meiklejohn_partisan, 2022_junior_performancepublish, 2023_peeroo_survey, 2026_paul_benchmarkingmessage
- provides: AMQP header size; Packet size ordering; Protocol choice recommendations

## Fiat-Shamir heuristic  [concept_fiat_shamir_heuristic]  (primitive; 5 papers)
The random evaluation point r for the automatic consistency proof can be derived non-interactively using Fiat–Shamir, as with randomness for the rand polynomials.
Papers: 2018_unger_deniable, 2019_sonnino_coconut, 2019_tyagi_messagefranking, 2023_agrawal_traceablemixnets, 2026_hafezi_aegon
- provides: Weak simulation extractability

## Side-Channel Attack  [concept_side_channel_attack]  (attack; 5 papers)
The server adversary may observe enclave control flow at instruction granularity and data accesses at byte granularity, potentially inferring client keys unless operations are oblivious.
Papers: 2018_wust_zlite, 2020_schwabe_kemtls, 2022_li_sok, 2024_jabbari_zk_dpps, 2024_nist_fips205
- attacks: Distributed Key Generation; Trusted Execution Environment
- leaks: SLH-DSA

## SPHINCS+  [concept_sphincs]  (system; 4 papers)
A stateless hash-based signature scheme. With n=256, h=63, d=9, b=12, k=29, w=16 and simple SHA-256 tweakable hashes, its signatures are 28% smaller than Picnic2’s average and 39% smaller than Picnic2’s worst case; signing is over 70% faster, key generation much slower, and verification almost 50 times faster.
Papers: 2019_bernstein_sphincsplus, 2020_sikeridis_pq_tls_performance, 2024_juaristi_pq_ethereum, 2024_nist_fips205
- instance_of: NIST post-quantum standardization competition
- measures: Parameterized signature comparison
- proves: Quantum random oracle model
- uses: SHA-256

## PowerMix  [concept_powermix]  (protocol; 4 papers)
An algebraic shuffling method with a single online round and asymptotically N^(3/2) scalar multiplications between shared and public values. The chunk reports that this becomes prohibitive at 2048 messages in hbMPC with 4 servers.
Papers: 2019_lu_asynchromix, 2020_abraham_blinder, 2023_sasy_sokmetadata, 2026_tang_dumbomix
- compares_with: Offline preprocessing cost; Switching network
- measures: PowerMix bandwidth; PowerMix latency; PowerMix latency tradeoff
- provides: PowerMix complexity
- uses: AMPC offline–online paradigm; Compute powers preprocessing; Message tag collision

## EC-based Schnorr signature  [concept_schnorr_signature]  (primitive; 4 papers)
The interactive Schnorr proof lets a prover demonstrate knowledge of private key k for public key K without revealing k; the Fiat-Shamir transform makes a hash-challenged proof non-interactive and publicly verifiable.
Papers: 2019_malina_secure, 2020_alonso_zerotomonero, 2020_yu_stealthschemes, nostr_nip_01
- compares_with: ComSig

## Clover  [concept_clover]  (protocol; 1 papers)
Anonymous transaction relay protocol for Bitcoin that randomly selects proxies for each relay operation, uses all connected peers, and sends transactions directly during proxying with one extra message per hop.
Papers: 2021_franzoni_clover
- assumes: Eavesdropper adversary
- compares_with: Clover versus Dandelion++ precision; Dandelion; Dandelion++
- defends_against: Multiple-unreachable-peer attack
- improves_on: Proxy-hop delay ratio
- instance_of: Simulation setup
- measures: Average hops by broadcast probability; Clover proxy precision at p=0.1; Clover proxy precision at p=0.2; Clover proxy precision at p=0.3
- provides: One extra message per proxy hop; Reachable-node coverage
- uses: Diffusing phase; Diffusion; First-Spy Estimator; Outbound-peer-only mixing; Proxy transaction distribution; Proxying; Proxying phase; Random proxy selection; Transaction mixing

## Messaging Layer Security (MLS)  [concept_messaging_layer_security]  (protocol; 4 papers)
A group messaging protocol based on the CGKA approach and TreeKEM, with cryptographic administration extension proposed in this work. Standard MLS relies on a centralized delivery service to order and distribute control messages.
Papers: 2022_balbas_a_cgka, 2025_auerbach_cgka_no_pruning, 2025_lebrun_thesis, 2026_mcmillion_keytrans_architecture
- compares_with: MLS-Cutoff
- contradicts: CGKA administration
- requires: Central delivery service
- uses: Continuous Group Key Agreement (CGKA); Forward Secure Group AEAD (FS-GAEAD); PRF-PRNG; TreeKEM; Unlinkable client credentials

## Updatable Public-Key Encryption (UPKE)  [concept_updatable_public_key_encryption]  (primitive; 3 papers)
A triple of algorithms (Gen, Enc, Dec) that updates the receiver’s key pair as messages are sent. If secret key sk_j is corrupted, ciphertexts c_i for i<j should remain hidden, even with adversarial randomness for those earlier ciphertexts, provided randomness for c_j is uniform and hidden.
Papers: 2022_bienstock_dr_uc, iog_modular_design_of_secure_group_messaging_protocols_and_the_s, iog_security_analysis_and_improvements_for_the_ietf_mls_standard
- assumes: UPKE pre-challenge randomness exposure
- provides: IND-CPA Security for UPKE; UPKE IND-CPA game; UPKE correctness; UPKE version advancement protects old plaintexts

## BACAP  [concept_bacap]  (protocol; 3 papers)
Blinding-and-Capability scheme derives pseudorandom sequences of single-use box IDs and keys for unlinkable messaging, with read and write capabilities and universally verifiable signatures.
Papers: 2025_infeld_echomix, spec_katzenpost_groupchat, spec_katzenpost_pigeonhole
- contradicts: BACAP post-compromise limits
- provides: BACAP box structure; BACAP read/write capabilities; BACAP sequence capacity; MembershipCap; Post-Quantum Forward-Security; Unlinkability
- uses: AES-256-GCM-SIV; BACAP KDF state; BACAP context binding; BACAP payload encryption and signature; Ed25519

## Zswap  [concept_zswap]  (protocol; 1 papers)
A zk-SNARK-based multi-asset transaction scheme for private transfers and non-interactive atomic swaps. It permits off-chain transaction merging while preserving anonymity.
Papers: iog_zswap_zk_snark_based_non_interactive_multi_asset_swaps
- compares_with: Mock Sapling; Proof of Stake; Proof of Work; Sapling
- defends_against: Front-running / Miner Extractable Value
- extends: Zcash Sapling
- improves_on: SwapCT
- measures: Zswap performance overhead
- provides: Atomic multi-asset swaps; Non-interactive transaction merging
- requires: HID-OR; One-Time Account (OTA); Trusted or transparent setup
- uses: Groth16; One-Time Account (OTA); POSEIDON; Simulation-extractable NIZK signatures; Single global ring; Sparse Homomorphic Commitments; zk-SNARK

## Double spending  [concept_double_spending]  (attack; 5 papers)
Two colluding accounts can craft receiver and amount ciphertexts that decrypt under both intended and colluder keys, passing the transaction proof while crediting an extra amount v′ to the colluder. Expected work is O(|WKE.pkr| + |v|) WKE encryptions and decryptions.
Papers: 2002_back_hashcash, 2019_rohrer_kadcast, 2023_bicer_ohe, 2024_hansen_ocash, iog_ouroboros_crypsinous_privacy_preserving_proof_of_stake
- attacks: PriFHEte architecture

## SybilRank  [concept_sybilrank]  (system; 1 papers)
Ranks accounts by perceived likelihood of being fake using trust propagation and degree-normalized trust. In the 160M-node synthetic graph, it completed in under 33 hours on 11 m1.large EC2 instances.
Papers: 2012_cao_sybilrank
- defends_against: Sybil Attack; targeted attack performance
- implements: MapReduce implementation
- improves_on: Detection improvement; Tuenti manual review hours
- measures: Facebook AUC at 1500 edges; Overall computational cost; Tuenti bottom sample result; Tuenti deployment precision; Tuenti processing time
- provides: Manual verification and CAPTCHA; SybilRank comparison result; random attack edge bound; uniform non-Sybil trust result
- requires: Bilateral social graph
- uses: degree bias removal; early termination trust distribution; log n power iterations

## ntrutor  [concept_ntrutor]  (protocol; 1 papers)
A minimal-change ntor variant that runs NTRUEncrypt key exchange in parallel with ntor, targeting 128-bit security and forward quantum-resistance. It keeps ntor's forward secrecy and one-way anonymity under the stated assumptions.
Papers: 2015_zhang_tor_quantum_handshake
- assumes: Fresh session condition
- contradicts: Active quantum adversary gap; Quantum resistance
- extends: ntor
- implements: Tor; ntrutor message flow
- measures: Client computation share; Client overhead; Handshake bandwidth; Handshake computation time; Handshake size; Router load
- provides: Anonymity; Forward Secrecy; Forward quantum-resistance; One-way anonymity; One-way authenticity; Weak multiple CCA security; ntrutor compromise tolerance
- requires: Random oracle KDF
- uses: Curve25519; Diffie-Hellman; NTRU key and ciphertext simulation; NTRUEncrypt

## Partitioning oracle attacks  [concept_partitioning_oracle_attack]  (attack; 2 papers)
An adaptive attack uses ciphertexts that decrypt successfully for subsets of candidate keys, then narrows the key set from oracle responses and finishes by binary search. In a 2^30-key simulation, bandwidth was about 3.44 GB for 20% success and 10.3 GB for 60%, versus 3.65 GB and about 11 GB for brute force.
Papers: 2016_hopwood_zcash_protocol_spec, 2021_len_partitioningoracle
- assumes: Known candidate secret set
- attacks: Anonymous communication system (ACS); OPAQUE; Shadowsocks
- compares_with: Padding oracle attacks
- provides: AES-GCM key recovery query bound; Binary partition queries
- requires: Observable decryption result
- uses: Key multi-collisions; Timing side-channels

## Partisan  [concept_partisan]  (system; 1 papers)
A distributed programming model and Erlang distribution layer that lets users specify cluster topologies at runtime without changing application code. Its default topology uses channels to exploit parallelism under high concurrency or latency.
Papers: 2018_meiklejohn_partisan
- compares_with: Distributed Erlang
- contradicts: Process Identifier Translation
- implements: Client-Server Topology; Full Mesh Topology; Partisan Publish-Subscribe Backend; Peer-to-Peer Topology; Static Membership
- improves_on: Distributed Erlang; Riak Core
- instance_of: Erlang
- measures: Channel Gain; Database Gain; Echo Service Gain; Parallelism Gain; Raw Distribution Benchmark
- provides: Best-Effort Delivery; Publish/Subscribe; Runtime Topology Selection
- uses: Channel parallelism; Channels; Connection Cache

## Erlay  [concept_erlay]  (protocol; 1 papers)
Bitcoin transaction relay combines low-fanout flooding with set reconciliation. It reduces relay bandwidth while accepting higher latency.
Papers: 2018_naumenko_erlay
- compares_with: BTCFlood; Dandelion; First-Spy Estimator; Short transaction identifiers
- defends_against: Sybil timing attack
- extends: Dandelion compatibility
- improves_on: Announcement bandwidth share; Public-spy attack cost
- measures: Black-hole slowdown; Evaluation setup; Fallback probability; Latency overhead; Prototype bandwidth and latency; Prototype results; Set difference estimate accuracy; Sketch decode time
- proves: Transaction-rate scaling
- provides: Bandwidth breakdown
- uses: High-rate bisection; Minisketch; Random response delay; Reconciliation fallback

## WTF-PAD  [concept_wtf_pad]  (defense; 3 papers)
A Tor website-fingerprinting defense based on adaptive padding that adds padding during low channel usage to mask bursts. It adds about 54% bandwidth overhead and no latency overhead; DF still reaches 90% closed-world accuracy.
Papers: 2018_sirinam_deepfingerprinting, 2020_gong_front, 2020_rahman_tiktok
- compares_with: FT-1 versus WTF-PAD
- defends_against: Deep Fingerprinting (DF); Timing information attack
- improves_on: BuFLO-family overhead; Tor
- leaks: Joint feature leakage
- measures: Closed-world DF accuracy; Defense bandwidth and latency overheads; Open-world DF scores; Open-world precision and recall; WeFDE information leakage
- uses: Dummy packets and delays

## Keyword PIR  [concept_keyword_pir]  (protocol; 4 papers)
Keyword PIR retrieves the value associated with a requested key from a key-value database. The server should learn no information about the queried key; for batch queries, it should learn no information about the queried key set.
Papers: 2019_ali_pircommcomp, 2023_ahmad_pantheon, 2023_patel_keywordpirsparse, 2024_tovey_distributedpir
- contradicts: Single-round consistency
- instance_of: Private Information Retrieval
- measures: Keyword-PIR round-trips
- provides: Password checkup application
- requires: Keyword-PIR requirements
- uses: Cuckoo-hashing keyword PIR; Simple-hashing keyword PIR

## 2PPS  [concept_2pps]  (protocol; 1 papers)
Twice-Private Publish-Subscribe provides publisher and subscriber unobservability using DPF-based secret sharing for publishing and ITPIR for subscribing. It is claimed to scale to 100,000 concurrent active clients at 5 seconds end-to-end latency.
Papers: 2021_2pps_pubsubprivacy
- assumes: Global network adversary
- compares_with: Blinder; Pung; Riffle; Riposte
- instance_of: Publish/Subscribe
- provides: Publisher Unobservability; Subscriber Unobservability
- requires: One honest server
- uses: Distributed Point Function; Encrypted DPF shares; Express; Full server database copies; Private Information Retrieval; Proxy relay; Subscription cover requests; Synchronized rounds

## Cardano  [concept_cardano]  (system; 5 papers)
The text gives two eclipse-related approaches in Cardano: dedicate connections to publicly known, registered Stake Pool Operator nodes, and locally detect eclipse state from block frequency and contents before leaving and rejoining.
Papers: 2021_cip20_tx_message, 2022_cip83_encrypted_metadata, iog_cougar_fast_and_eclipse_resilient_dissemination_for_blockcha, iog_message_passing_in_the_extended_utxo_ledger_model, iog_securecyclon_dependable_peer_sampling
- implements: Metadata label 674
- instance_of: EUTxO ledger model
- provides: Block component sizes; Transaction metadata visibility
- uses: Local eclipse detection; Trusted peer connections

## SEEMless  [concept_seemless]  (system; 5 papers)
SEEMless is cited as a VKD style where auditing append-onlyness verifies tree paths for inserted keys. Reported costs are for 10 million users with 1,000 additions and 1,000 updates per epoch.
Papers: 2022_tzialla_transparencydictionaries, 2024_brandt_kt_sok, 2024_brorsson_consistency_or_die, 2024_len_elektra, 2026_hafezi_aegon
- contradicts: Lookup soundness
- leaks: AKD lookup leakage

## TreePIR  [concept_treepir]  (protocol; 2 papers)
A private information retrieval scheme that maps index x to components xℓ and xr using concatenation and splitting when N is a perfect square and a power of two. The chunk says it can be generalized to any perfect-square N with extra steps.
Papers: 2023_lazzaretti_treepir, 2024_lazzaretti_singlepasspir
- assumes: Square power-of-two database size assumption
- compares_with: Checklist; Checklist repeated-query degradation; PRP-PIR; Privately puncturable PRF bandwidth estimate
- extends: Shift optimization
- implements: Two-server separation
- instance_of: Private Information Retrieval
- measures: Client key sampling cost; Large bit database benchmark; Large database benchmark; Medium database benchmark
- proves: Recursive PIR result
- provides: Generalized index mapping; Set-size tradeoff D; TreePIR complexity bounds
- requires: Coverage failure probability
- uses: Single-server recursion; Waterfall update approach; wpPRF

## POPRF  [concept_poprf]  (protocol; 1 papers)
Accepts client-private input and shared public input info, binding the latter to the output while hiding the private input, output, and server key. Its stated security relies on One-More Gap SDHI.
Papers: 2023_rfc9497_oprf
- assumes: One-More Gap SDHI assumption
- extends: OPRF
- measures: Batch test sizes
- provides: Output size; POPRF batch one vector one; POPRF batch one vector two; POPRF batch two vector; POPRF outputs; POPRF proof values
- requires: Server key derivation
- uses: POPRF blind values; POPRF input info; POPRF key setup; Public POPRF info; Public info key tweak; Serialized element size; Serialized scalar size

## Pirates  [concept_pirates]  (protocol; 1 papers)
Anonymous group voice-call protocol over fully untrusted infrastructure. It claims communication unobservability and supports groups of at most G members using PIR, fixed-size traffic, and mailbox retrieval.
Papers: 2024_coijanovic_pirates
- assumes: Benign uncompromised groups; Fixed preexisting groups; Global active adversary; Synchronous clocks
- improves_on: Addra
- leaks: Participation privacy non-goal
- measures: Single-server latency result
- provides: Availability under denial of service; Communication Unobservability
- requires: IND-CPA security; Maximum group size G; Preimage Resistance; Shared group master key GMK
- uses: Coordinator-relay-worker hierarchy; Cover Traffic; Epoch-specific deterministic invites; FastPIR; Fixed maximum query count; Multi-query PIR buckets; One invite per client per dialing phase; Per-client mailboxes; Private Information Retrieval

## Nakamoto consensus  [concept_nakamoto_consensus]  (protocol; 2 papers)
The target setting permits an arbitrarily large, shifting, untrusted set of parties, independent of platform performance parameters. Kachina requires no additional trust assumptions beyond Nakamoto consensus and a securely generated common reference string.
Papers: iog_full_analysis_of_nakamoto_consensus_in_bounded_delay_network, iog_kachina_foundations_of_private_smart_contracts
- assumes: Bounded-delay model; Dynamic partially synchronous setting
- proves: Common prefix; Consistency; Consistent timekeeping; Liveness
- provides: Failure probability
- requires: Bootstrapping timeout; Security conditions C1-C3; Timestamp forward parameter
- uses: Epoch target recalculation; Local clock adjustment; Proof of Work; Random oracle simulation; Timestamp validation; Unauthenticated gossip diffusion

## Phalanx  [concept_phalanx]  (protocol; 2 papers)
Verdict’s SNARK for epoch-based, data-parallel circuit satisfiability. It uses a SIMD R1CS folding scheme and Dory commitments to provide constant-size per-epoch proofs and verification, plus logarithmic-size running-instance proofs.
Papers: 2011_sarela_bloomcasting, 2022_tzialla_transparencydictionaries
- compares_with: Hyrax-PC; Phalanx (eager)
- hides: Reactive filtering
- improves_on: Merkle update proof cost; Phalanx versus Spartan
- measures: 128 updates, 2^24 labels; 2.3× prover overhead; SNARK parameter size
- provides: Over an order of magnitude savings; Two-epoch amortization threshold
- uses: Capability-based filtering; Dory polynomial commitments; Phalanx running instance; SIMD R1CS; SIMD folding scheme; Spartan; Sumcheck protocol

## Crowds  [concept_crowds]  (system; 3 papers)
An anonymity network that randomly routes user communications through a group of similar users, blending the sender among the crowd; the thesis lists predecessor, global-attacker, and local-eavesdropper vulnerabilities.
Papers: 2012_feigenbaum_onion_blackbox, 2012_mulamba_design, 2019_lu_survey
- attacks: Crowds anonymity attacks
- provides: Crowds degree-of-anonymity levels; Publisher and subscriber anonymity
- uses: Blender; Centralized Crowd membership; Fuzzy initiating edge; Jondo; Random forwarding and coin flip

## Anytrust assumption  [concept_anytrust]  (assumption; 3 papers)
Scalable DC-nets and several systems rely on anytrust, meaning privacy depends on at least one honest server in the relevant group or chain; the chunk warns that such split-trust assumptions can be silently subverted.
Papers: 2013_corrigangibbs_verdict, 2023_sasy_sokmetadata, 2026_li_pepper
- provides: Anonymity Set
- requires: Honest server hub

## Secure multi-party computation  [concept_secure_multi_party_computation]  (mechanism; 4 papers)
Computes an n-ary polynomial-time functionality while revealing only its result, even with some malicious parties; the chunk cites BGW for fewer than n/3 corruptions and GMW for any malicious minority.
Papers: 2013_gelernter_limits_provable_anonymity, 2013_zamani_anonymousbroadcast, 2022_shirali_dcnetsurvey, 2024_jabbari_zk_dpps
- compares_with: Sequential MPC mixing cost
- defends_against: Side-Channel Attack
- implements: Threshold key reconstruction
- proves: GMW theorem
- uses: Oblivious Transfer

## Zerocash  [concept_zerocash]  (system; 3 papers)
Kachina expresses Zerocash-style privacy-preserving payments as a contract over public shared and local private state; the paper says its case study UC-emulates a simpler ideal payments contract. No numeric cost results appear in this chunk.
Papers: 2014_bensasson_zerocash, 2026_cinal_viewingkeycompromise, iog_kachina_foundations_of_private_smart_contracts
- compares_with: Private payment leakage
- implements: Public serial number and commitment
- instance_of: Decentralized anonymous payment scheme
- leaks: Network metadata leakage
- measures: Receive algorithm cost; zk-SNARK proving cost; zk-SNARK runtime
- proves: Universal Composition (UC) model
- provides: Ledger indistinguishability; Private payment leakage
- uses: Private-state off-chain work; Zerocoin

## Garbled Circuits  [concept_garbled_circuits]  (primitive; 4 papers)
The sender garbles a circuit for f(R,M), encrypts both labels for each receiver input wire, and reveals the labels selected by M through the detection key. The paper modifies Yao garbling so wrong labels do not cause evaluation failure.
Papers: 2019_kales_contactdiscovery, 2021_beck_fmd, 2021_madathil_privatesignaling, 2022_jin_secure
- uses: Oblivious Transfer; Point-and-permute; Pseudorandom generator

## Classic McEliece  [concept_classic_mceliece]  (primitive; 5 papers)
The paper establishes C2PRI for Classic McEliece. Its specified standard parameter sets have ciphertexts from 96 to 208 bytes, suggesting more modest performance gains when omitted from derivation.
Papers: 2021_hashimoto_chained_cmpke, 2022_grubbs_anonrobustpq, 2022_xagawa_anonymitykems, 2024_rial_outfox, 2025_alagic_best_of_both_kems
- assumes: Strong disjoint-simulatability
- attacks: Universal Classic McEliece ciphertext
- compares_with: IND-CCA
- motivates: McEliece mobile-plan depletion
- provides: Ciphertext second preimage resistance (C2PRI)

## Pantheon  [concept_pantheon]  (system; 1 papers)
Private retrieval from a public key-value store using BFV homomorphic encryption for query privacy and PIR for value retrieval. The prototype has about 3,000 lines of C++ and is configured for 128-bit security.
Papers: 2023_ahmad_pantheon
- implements: Query compression; Single-round Get protocol
- measures: Cluster retrieval latency; Key size results; Single-machine retrieval latency; Tuple scaling results; Value size results
- provides: Equality multiplication reduction; Privacy leakage scope
- uses: BFV parameter configuration; Brakerski/Fan-Vercauteren (BFV); Coordinator-worker architecture; FastPIR; Fermat’s little theorem; Fully homomorphic encryption (FHE); Microsoft SEAL; Oblivious equality check; Private Information Retrieval; Public key-value store

## Dolev–Yao symbolic model  [concept_dolev_yao_model]  (concept; 5 papers)
Cryptographic operations are treated as perfect: ciphertext reveals no plaintext unless the attacker knows the decryption key. Knowing the corresponding key, for example through compromise, reveals the plaintext.
Papers: 2023_auerbach_pcs_cost_concurrent, 2024_matrix_symbolic, 2024_vac_adversarial_models, 2025_wallez_thesis, 2025_wallez_treekem_verified
- instance_of: Symbolic model
- measures: Analysis cluster resources; Megolm unknown key-share result

## Single-Use Reply Block  [concept_surb]  (primitive; 4 papers)
Single-use reply blocks provide recipient anonymity: a client gives a cryptographic delivery token to another client so it can send a reply without knowing the recipient's identity or network location.
Papers: 2023_kocaogullar_pudding, 2026_constantinides_hiddenservices, spec_katzenpost_mixnet, spec_katzenpost_pigeonhole
- attacks: Malicious first-mix-hop attack; Malicious last-mix-hop attack
- hides: Provider message-count leak
- provides: Anonymity; Client; Recipient anonymity

## Ordered Zero-Knowledge Sets  [concept_ordered_zero_knowledge_set]  (primitive; 3 papers)
Supports initialization, updates with commitments and proofs, and membership or non-membership queries that include the epoch a label was added. The weaker soundness used here prevents two verifying proofs for different values or epochs for one label under a commitment.
Papers: 2023_len_optiks, 2023_malvai_parakeet, 2024_ghosh_optiks_weak
- extends: Secure compaction
- implements: Merkle Patricia Trie (MPT)
- provides: Lookup privacy goal; oZKS space complexity
- uses: Append-only Strong Accumulator; Hiding commitment scheme; Simulatable Commitment Scheme; Simulatable Verifiable Random Function; Verifiable Random Function (VRF)

## FastDDS / FastRTPS  [concept_fastdds]  (system; 2 papers)
ROS 2 DDS implementation, used as the default since ROS 2 began; it adds shared-memory transport and is claimed to achieve under 20 µs delay for packets up to 15 kB and throughput on the order of 10^4 MB/s in ideal conditions.
Papers: 2024_chovet_performancecomparison, 2025_kluner_zenohautomotive
- compares_with: FastDDS and Cyclone comparison
- implements: Publish/Subscribe
- instance_of: Data Distribution Service (DDS)
- measures: FastDDS claimed delay; FastDDS claimed throughput
- provides: Security options
- uses: Multicast discovery; Reliable and best-effort modes; Topic and key matching

## OCash  [concept_ocash]  (system; 1 papers)
OCash is presented as an anonymous payment protocol for blockchain light clients. It uses a ledger, anonymous authenticated transfer, a service, and an SOROM to support coin payment and collection.
Papers: 2024_hansen_ocash
- assumes: Hybrid model
- defends_against: Full nodes
- implements: Ledger and anonymizer roles
- proves: Weak anonymity
- provides: Light clients; Polylogarithmic ledger access; Strong anonymity
- requires: Trusted anonymizer service
- uses: Anonymous blockchain coin flip; Anonymous coin friendly encryption; Balance commitment; Collection proofs; Compressible Randomness Beacon; Encrypted coin; Oblivious RAM; Oblivious map size; On-chain coin shuffling; SOROM coin mixing

## OnionPIRv2  [concept_onionpirv2]  (protocol; 1 papers)
An improved implementation of OnionPIR using standard FHE techniques and engineering changes. In the evaluated setting it uses 15 KB requests and 11 KB responses, with 3.7× response overhead for 3 KB entries and 1031–1372 MB/s server throughput.
Papers: 2025_chen_onionpirv2
- compares_with: KsPIR; Spiral
- extends: OnionPIR
- instance_of: Private Information Retrieval
- measures: Server computation throughput
- provides: Estimated security level; Modulus trade-off; Per-client server key storage; Request size; Response overhead; Response size
- uses: BV-style key switching; Composite NTT; Homomorphic operation costs; Matrix multiplication in initial dimension; Modulus switching; NTT database preprocessing; Non-uniform database dimensions; One external product per selection; Query packing; Separate decomposition parameters

## InsPIRe  [concept_inspire]  (protocol; 1 papers)
Single-server PIR in the CRS model with server-side preprocessing and no offline communication; targets high throughput and low query communication.
Papers: 2025_mahdavi_inspire
- assumes: Independence heuristic
- compares_with: DoublePIR; HintlessPIR; Piano; SimplePIR; YPIR
- defends_against: Per-client state correlation leak
- improves_on: Client hint update cost; Client-specific key storage cost; IPFS; YPIR query size
- instance_of: Private Information Retrieval
- measures: 32 GB database benchmark; Communication-focused parameterization; Device enrollment benchmark; IPFS application benchmark; Key size reduction vs YPIR; Online query communication vs YPIR
- provides: No offline communication; Query-index privacy
- uses: Common Reference String (CRS) model; Homomorphic polynomial evaluation; InspiRING

## Aegon  [concept_aegon]  (system; 1 papers)
A privacy-preserving transparent dictionary using the zero-knowledge variant of KZH; it aims for constant auditor cost and per-epoch server computation based on updates in that epoch.
Papers: 2026_hafezi_aegon
- assumes: Honest auditor per epoch assumption
- improves_on: IronDict; Lookup efficiency gain
- instance_of: Transparent dictionary
- measures: Publish throughput
- proves: UC-based dictionary privacy definition
- provides: Aegon audit privacy; Aegon auditor proof; Auditor Cost Depends on Shards; Client query proofs; Per-Epoch Server Workload
- requires: Zero Knowledge
- uses: Client-delegated index uniqueness; Dictionary sharding; Historical Lookup Precomputation; KZH; Polynomial commitment scheme (PCS); Proof caching; Two-Polynomial Dictionary; Zero-Knowledge Proof

## mpOTR  [concept_mpotr]  (protocol; 2 papers)
Uses deniable group key exchange to give participants identity proof that outsiders cannot use to convince others. All parties must be online for setup; shared ephemeral signing keys preserve message repudiation but prevent message unlinkability, and group membership changes require a new exchange.
Papers: 2009_goldberg_mpotr, 2015_unger_sok_securemessaging_tr
- defends_against: Malicious insiders; Privacy adversary M
- extends: Off-the-Record Messaging (OTR)
- leaks: Anonymity
- provides: Anonymity; Confidentiality; Deniability; Forward Secrecy; Transcript consensus
- requires: Network communication primitives; Pseudonymity
- uses: End-of-conversation consistency check; Ephemeral key derivation; Ephemeral session signature keys; Pairwise participant authentication; Session identifier; Shared chat encryption key

## TCP  [concept_tcp]  (protocol; 5 papers)
The latency model assumes TCP with established connections and adapted window scaling. Under those assumptions and without retransmissions, small-message transmission is close to half the RTT; typical Ethernet MTU is 1.5 KB.
Papers: 2011_malekpour_endtoend, 2019_banno_interworking_layer, 2023_jami_swarm_drt_docs, 2023_peeroo_survey, 2024_revuelta_waku_latency
- assumes: Small-message transmission assumption
- provides: Neighbor failure recovery

## Synapse  [concept_synapse]  (protocol; 1 papers)
Synapse is a generic meta-protocol for retrieval across heterogeneous overlays, using co-located peers as distributed gateways and opportunistic forwarding; its routing is unstructured and non-exhaustive.
Papers: 2013_ciancaglini_keybased
- assumes: Synapse network assumptions
- implements: Co-located Synapse nodes
- measures: Synapse overhead scaling
- provides: Alternate-path partition resilience; Black-box Synapse; White-box Synapse
- requires: Scalability condition
- uses: Co-located Synapse nodes; Maximum Replication Rate; Stateless 1-Random-Walk; TTL and session identifiers; good_deal? policy

## Least Squares Disclosure Attack (LSDA)  [concept_least_squares_disclosure_attack]  (attack; 2 papers)
LSDA estimates sender–receiver transition probabilities from per-round sent and received message counts by solving a least-squares problem. It profiles persistent communication relationships; its estimator is unbiased and asymptotically efficient when all messages leave each round.
Papers: 2013_oya_sda_family, 2014_oya_real_world_sda
- attacks: Mix
- compares_with: SDA2 estimator
- implements: LSDA linear system
- measures: Mean squared error; Sending profiles; Transition probabilities
- requires: Observation window
- uses: Per-round input counts; Per-round output counts

## Asymmetric Scalar-product Preserving Encryption (ASPE)  [concept_asymmetric_scalar_product_preserving_encryption]  (primitive; 3 papers)
Asymmetric scalar product-preserving encryption represents publication attributes and subscription constraints as multidimensional points, supports containment, and is vulnerable to known-plaintext attacks. Its matching complexity is prohibitively high with many attributes.
Papers: 2014_onica_efficient, 2016_onica_confidentialitypreserving, 2016_pires_secure
- contradicts: Event and filter confidentiality
- implements: ASPE encrypted distance comparison
- improves_on: ASPE pre-filtering
- instance_of: Relation-preserving isomorphism matching
- provides: Containment-based filtering
- uses: ASPE random symmetric subscription split; Symmetric reference subscription points

## Certificate Transparency  [concept_certificate_transparency]  (protocol; 5 papers)
Requires all issued web certificates to enter a public append-only signed Merkle tree with continual consistency proofs; certificates are trusted only with cryptographic proof of inclusion.
Papers: 2015_unger_sok_securemessaging_tr, 2020_sikeridis_pq_tls_performance, 2021_hu_merkle2, 2022_henzinger_simplepir, 2026_mcmillion_keytrans_architecture
- instance_of: Transparency logs
- uses: Chronological tree

## Chinese Remainder Theorem (CRT)  [concept_chinese_remainder_theorem]  (primitive; 5 papers)
CRT representation makes polynomial multiplication cost linear in log p rather than quadratic, but integer conversion to and from CRT costs quadratic in log p. CRT lifting during decryption requires multiprecision arithmetic for multiple moduli.
Papers: 2016_aguilarmelchor_xpir, 2019_ali_pircommcomp, 2023_li_hintlesspir, 2025_chen_onionpirv2, 2025_gidney_rsa_million_qubits

## DDoS attack  [concept_ddos_attack]  (attack; 4 papers)
The paper examines distributed denial-of-service attacks against stateless forwarding, including attacks that flood network resources or target end users by exploiting forwarding behavior.
Papers: 2016_alzahrani_proactive, 2021_tian_iot_pubsub_access_control, 2024_heimbach_deanon, 2025_li_dpsiiot
- attacks: Blockchain
- provides: One-third propagation disruption

## AnonPoP  [concept_anon_pop]  (system; 1 papers)
A practical anonymous messaging system that combines a synchronous mix cascade, constant sending rate, request pools, bad server isolation and per epoch mailboxes. The paper claims support for mobile clients, costs below $0.25 per client per year, and two cents per month.
Papers: 2016_gelernter_anonpop
- assumes: Malicious server bound f; Secure initial key exchange; Trusted directory service
- compares_with: Latency and overhead tradeoff
- defends_against: Global eavesdropper
- measures: Monthly cost per client
- proves: De-anonymization query bound
- provides: Attacker isolation functions; Forward secrecy; Mobile suitability; Passive anonymity claim; Proactive security; Unobservability claim
- uses: Bad server isolation; Fixed rate envelopes; Mixnet; Onion Routing; Per-epoch mailboxes; Post-Office servers; Request pool; Tag prevention

## VPN  [concept_vpn]  (system; 5 papers)
A centralized encrypted tunnel forwards user communications through a provider that can observe all traffic and destinations. A local observer at the server can correlate ingress and egress, deanonymize users, or block access.
Papers: 2017_barman_prifi, 2020_bahramali_practical, 2021_diaz_nym, 2023_kosaka_mqttcontrol, 2026_zhang_bitcoin_trafficanalysis
- defends_against: Event-based detector
- instance_of: Circumvention experiment
- provides: Tor or VPN mitigation

## Ratcheted Key Exchange (RKE)  [concept_ratcheted_key_exchange]  (protocol; 2 papers)
RKE combines updatable, randomizable public-key encryption and one-time signatures with a pseudorandom generator and random oracle. This chunk proves recovery, authenticity, key-indistinguishability, and anonymity results for the construction.
Papers: 2018_poettering_asynchronous_rke, 2022_dowling_anonymous_rke
- implements: Receiver state update; Sender state update
- instance_of: Bidirectional Ratcheted Key Exchange (BRKE); Sesquidirectional Ratcheted Key Exchange (SRKE); Unidirectional Ratcheted Key Exchange (URKE)
- provides: Generic-primitive construction approach
- requires: urPKE; urSIG
- uses: Message authentication code (MAC); One-time signature; PRG; Random oracle simulation

## Tithonus  [concept_tithonus]  (system; 1 papers)
A Bitcoin based censorship resistant communication framework carrying client requests in inconspicuous transactions propagated by gossip; it reports transfer cost about 100 times lower and goodput 1,000–100,000 times higher than state-of-the-art Bitcoin writing solutions.
Papers: 2018_recabarren_tithonus
- assumes: Censor capability assumptions; Full-node security tradeoff; Service trust assumption; Sybil Attack
- compares_with: Publish/Subscribe
- defends_against: Denial of service attack; Eclipse Attack
- provides: Censorship resistance; Unobservability
- uses: BitTorrent; Bitcoin gossip propagation; Bloom Filter; Certificate chain of trust; Client registration message; ECIES; Hidden sequencing; On-chain transactions; Payments prevent DoS; Staged transactions

## Merkle²  [concept_merkle2]  (system; 2 papers)
A transparency log with nested chronological and prefix Merkle trees, efficient monitoring and lookup, and low-latency updates. Its operations are polylogarithmic in log entries and independent of update intervals.
Papers: 2021_hu_merkle2, 2022_tzialla_transparencydictionaries
- compares_with: Append and lookup tradeoff; One-hour epoch comparison
- improves_on: CONIKS
- measures: Append cost; Lookup cost; One-second epoch setting; Storage cost; Update propagation latency
- provides: Digest size; Owner monitoring cost
- uses: Chronological tree; Extension proof; Pre-build strategy; Prefix tree; Signature chains

## AOT (Anonymization by Oblivious Transfer)  [concept_aot]  (system; 1 papers)
A three-level mixnet uses oblivious transfer (OT) for message delivery. The chunk says OT helps resist blending (n−1) attacks and preserve receiver anonymity even if a covert adversary controls all AOT nodes.
Papers: 2021_javani_aot
- assumes: Dolev–Yao network intruder
- implements: Three-level cascade
- instance_of: Mixnet
- measures: Expected publication time; OT throughput benchmark
- provides: Anonymous shared-secret handshake; Message-integrity goal; Receiver anonymity under full network compromise; Resending after node failure
- uses: Counter synchronization window ξ; Dummy-message volume; Fixed-size payloads and tags; Loop-message integrity check; OT session size ζ; Oblivious Transfer; Perfectly hiding commitment; Publication parameters λ, τ, γ; Replay-detection window T; Shared-secret message tags

## Kafka  [concept_kafka]  (system; 3 papers)
The next chapter introduces Kafka as an event-streaming publish/subscribe system with broker storage for a predefined period, asynchronous communication, replay, larger data volumes, replication, and fault tolerance. This chunk only begins describing Kafka and Zookeeper.
Papers: 2022_berjon_eventmesh, 2022_klingler_confidentialite, 2023_liang_zenohperformance
- instance_of: Storage brokers; Topic-Based Pub/Sub
- measures: Multi-machine latency results; Multi-machine throughput results; Single-machine Kafka and MQTT limits; Single-machine latency results
- requires: Apache Zookeeper
- uses: Broker-relay topology; Kafka acknowledgement tradeoff; Kafka benchmark settings; Kafka partition replication

## FO transform  [concept_fo_transform]  (mechanism; 3 papers)
The paper analyzes FO transform variants, including explicit- and implicit-rejection forms, to derive KEM anonymity, pseudorandomness, smoothness, and collision-freeness from assumptions on the underlying PKE.
Papers: 2022_grubbs_anonrobustpq, 2022_xagawa_anonymitykems, 2023_cremers_keeping_up_kems
- implements: Key Encapsulation Mechanism
- provides: Collision-freeness; IND-CCA
- requires: Strong disjoint-simulatability

## SPR-CCA security  [concept_spr_cca_security]  (property; 2 papers)
Strong pseudorandomness under chosen-ciphertext attack is the premise used to prove anonymity and the principal target property for hybrid encryption and NTRU.
Papers: 2022_maram_pq_anonymity_kyber, 2022_xagawa_anonymitykems
- proves: ANO-CCA security; ANON-CCA security; Theorem 2 SPR-CCA bound
- provides: Kyber.KEM
- requires: Ciphertext indistinguishability; Statistical disjointness; Strong disjoint simulatability; δ-correctness

## Anonymous Credit Tokens (ACT)  [concept_anonymous_credit_tokens]  (protocol; 1 papers)
An authentication protocol for numerical credits, using keyed-verification anonymous credentials and privately verifiable BBS-style signatures. Issuers grant credits that clients can spend anonymously with that issuer.
Papers: 2026_draft_act
- implements: Setup, issuance, and spending
- motivates: Rate limiting and API credits
- provides: Anonymous change token; Balance privacy; Partial credit return; Partial spending; Point and scalar encoding size; Unlinkability; Zero-spend re-anonymization
- requires: Credit bit length L; Deployment domain separator; Deterministic independent generators; Used-nullifier state
- uses: BBS signature scheme; BLAKE3; Fiat–Shamir transform; Keyed-verification anonymous credentials (KVAC); Length-prefixed transcripts; Rate-Limiting Nullifier; Request context; Ristretto255 group; Sigma protocol

## Mixminion  [concept_mixminion]  (system; 5 papers)
Type III remailer using synchronized redundant directory servers, timed dynamic pool flushing, reply blocks and single-use reply blocks (SURBs). Its route has two legs; sender and recipient each choose half for replies, while crossover and exit mixes have partial content knowledge.
Papers: 2009_danezis_sphinx, 2015_unger_sok_securemessaging, 2015_unger_sok_securemessaging_tr, 2018_shirazi_survey_routing_anon, 2026_davitt_mixnetusability
- instance_of: Mixnet; Transport privacy layer
- uses: Pool mixes; Single-use reply block

## Confidentiality  [concept_confidentiality]  (property; 4 papers)
For qualifying packets, the adversary learns no information about an encryption layer assigned to an honest party if it neither receives that layer nor obtains it by processing another layer. The stated guarantee applies to honest-sender requests and replies based on an honest sender's reply block.
Papers: 2009_goldberg_mpotr, 2020_pozo_evaluation, 2021_vac_waku2_payload_spec, 2024_rial_outfox
- leaks: Transcript length and traffic pattern leakage

## FireSpam  [concept_firespam]  (protocol; 1 papers)
A spam-resilient gossip protocol organizes nodes in a ladder by filtering capability and disseminates messages from the bottom upward. It is designed for Byzantine and rational behavior and is built on Fireflies.
Papers: 2011_pace_gossiping
- assumes: BAR model; Classification error below five percent; FireSpam network assumptions; Rational-node utility
- compares_with: RandCast
- defends_against: Eclipse resilience result
- implements: Filtering-capability ladder
- improves_on: No comprehensive spam-resilient solution
- measures: Bandwidth evaluation announced; FireSpam simulation findings; Ladder latency tradeoff; Spam reduction by filtering capability
- proves: FireSpam strict Nash equilibrium result; Strict Nash equilibrium claim
- uses: Fireflies; Forwarding view; Good, spam, and undetermined classes; Node monitors; Publication view

## FlightPath  [concept_flightpath]  (protocol; 3 papers)
FlightPath is the only evaluated system said to implement defenses against selfish behaviour, using the BAR model. It supports one streaming source per multicast group and depends on a tracker whose malicious or selfish behaviour prevents guaranteed reliability.
Papers: 2011_pace_gossiping, 2013_rene_erreichen, 2015_decouchant_collusions
- defends_against: Information leak; Message tampering
- extends: BAR Gossip
- improves_on: Nash equilibrium
- measures: Simple Comprehensive Reliability Evaluation model
- uses: Age-organized tubs; Epoch-based membership; Erasure coding; Imbalance ratio α; Split demands among partners; Subscription matching; Tail inversion; Trade-count tradeoff

## Sniper Attack  [concept_sniper_attack]  (attack; 2 papers)
A malicious client sends SENDME signals without reading data, causing exit relays to send more data and eventually exhausting entry-relay memory until the OS terminates it. Requires client modification.
Papers: 2014_jansen_sniper, 2017_kim_sgxtor
- implements: Guard reselection deanonymization
- measures: 50-relay evaluation; Directory authority disable time; Median sniper bandwidth; Median target RAM rates; Prototype resource maxima; Relay disable time estimates; Sniper RAM per Tor instance
- provides: Relay path failure impact
- uses: Anonymous six-relay path; Default attack configuration; Experiment timing

## Key-updatable KEM (kuKEM)  [concept_key_updatable_kem]  (primitive; 2 papers)
A KEM with deterministic updates to secret or public keys using associated data. Compatiblely updated key pairs still decapsulate correctly; its security notion requires encapsulated keys to remain hidden after incompatible receiver-key updates or exposure.
Papers: 2018_poettering_asynchronous_rke, 2023_rosler_upibe
- compares_with: UPIBE and KU-KEM relationship
- implements: Hierarchical Identity-Based Encryption (HIBE)
- motivates: Bare-DLP kuKEM open problem
- proves: KU-KEM one-wayness reduction
- provides: Effective divergence; KU-KEM forward secrecy; kuKEM forward-security condition
- uses: Associated-data key updates; Hierarchical identity-based encryption (HIBE); KU-KEM from UPIBE construction

## Elliptic curve cryptography  [concept_elliptic_curve_cryptography]  (primitive; 4 papers)
The paper uses asymmetric ECC keys for publisher and subscriber encryption, decryption, and validation. It claims smaller keys, ciphertext, and signatures, and shorter key-generation and signature times than RSA for equal security, without giving numeric sizes or timings.
Papers: 2019_burgel_hopr, 2020_alonso_zerotomonero, 2026_gajji_blockchainenabled, 2026_mallick_aquaman
- assumes: Discrete Logarithm Problem
- implements: ECC shared-secret message encryption
- improves_on: Twisted Edwards efficiency
- provides: Cyclic subgroups and cofactor

## Autocrypt Level 1  [concept_autocrypt]  (protocol; 2 papers)
Opportunistic end-to-end encrypted email with automatic, decentralized in-band key distribution. Level 1 defends against passive data collection; protection from active message modification is deferred to future specifications.
Papers: 2020_autocrypt_spec_1_1, 2024_song_deltachat
- assumes: Passive adversary scope
- uses: Autocrypt email headers; Autocrypt key gossip; Cv25519; Decentralized in-band key distribution; Ed25519; OpenPGP; Opportunistic encryption policy

## MQTT-ST  [concept_mqtt_st]  (protocol; 1 papers)
A protocol that automatically interconnects MQTT brokers in a dynamic loop-free spanning tree, with full message replication and reaction to failures. It reuses MQTT control messages and is implemented on Eclipse Mosquitto.
Papers: 2020_longo_mqtt_st
- compares_with: Centralized Broker
- defends_against: Looping Bridge Messages
- extends: MQTT
- implements: Broker Connection Handshake; Failure Recovery; Forwarding Tree
- improves_on: Local Publication Throughput; Network Latency Improvement
- instance_of: Publish/Subscribe
- measures: Local End-to-End Delay; Signalling Message Size
- provides: Full Message Replication
- uses: Broker Capability Score; Connection Table; In-Band Signalling; Last Will Forwarding; Latency Path Cost; Message Flooding; PINGREQ Signalling Fields; Spanning Tree Protocol

## Non-interactive zero-knowledge proof  [concept_non_interactive_zero_knowledge]  (primitive; 3 papers)
NIZK proves that a transaction transcript is consistent with Γ and its input; verification requires short public transcript, input, and private transcript, and Γ efficiently expressible in the underlying ZK system.
Papers: 2021_agrawal_lattice_blind_sig, 2021_hashimoto_pq_x3dh_deniable, iog_kachina_foundations_of_private_smart_contracts
- provides: Deniability
- requires: Efficient NIZK statement condition
- uses: Authenticated key exchange

## FastPIR  [concept_fastpir]  (protocol; 3 papers)
Pantheon’s selected PIR library, parallelized for its server-side PIR step because it requires lower response-generation processing time and uses vectorized BFV. PIR time grows linearly with value size and with a slope below 1 as tuple count grows.
Papers: 2021_ahmad_addra, 2023_ahmad_pantheon, 2024_coijanovic_pirates
- implements: Compressed PIR query processing; Packed PIR responses
- improves_on: CPIR recursion tradeoff
- proves: FastPIR crossover threshold
- provides: Additive response aggregation
- requires: BFV rotation key sizes
- uses: Brakerski/Fan-Vercauteren (BFV)

## Verifiable Key Directory (VKD)  [concept_verifiable_key_directory]  (primitive; 3 papers)
Stores evolving label-value pairs, commits to the set, and answers client queries and update checks with cryptographic proofs; values are public keys. Privacy is zero knowledge with a defined leakage function.
Papers: 2023_malvai_parakeet, 2024_brorsson_consistency_or_die, 2024_len_elektra
- proves: Non-equivocation
- provides: Non-equivocation; VKD privacy and leakage
- uses: Ordered Zero-Knowledge Sets; StorageAPI
