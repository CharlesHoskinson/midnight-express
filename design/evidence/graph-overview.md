# Graph overview

The 90 largest communities of the corpus graph, with a one-sentence summary and the most connected members. Use `design/evidence/graph-digest.md` for named concepts and `design/evidence/papers.tsv` for the paper index.

## Decentralized Publish-Subscribe Overlays  (392 nodes)
The cluster covers peer-to-peer publish/subscribe systems and overlay-based content dissemination, including routing, reliability, causal ordering, and anonymity trade-offs.
Key nodes: Publish/Subscribe; OpenPubSub: Supporting Large Semantic Content Spac; Confidentialité et traçabilité dans les systèmes p; Techniques for building a scalable and reliable di; Efficient dissemination in decentralized social ne; Leveraging a Publish/Subscribe Fog System to Provi; An efficient causal group communication protocol f; Immediate Dependency Relation; JTangCSPS; PastryStrings
Example papers: 1998-chor-pir, 2011-mega-dissemination-decentralized, 2011-shapiro-conflictfree, 2011-singh-disclosurecontrol, 2012-lahyani-manetanalytical, 2012-zuzak-performancehierarchical

## GossipSub Protocol and Security  (282 nodes)
This cluster covers GossipSub’s design, peer scoring, spam protection, security evaluation, and performance for decentralized message dissemination.
Key nodes: GossipSub; Peer Scoring; GossipSub: A Secure PubSub Protocol for Unstructur; Privacy-Preserving Spam-Protected Gossip-Based Rou; Gossipsub v1.1 Protocol Design + Implementation Se; Staggering and Fragmentation for Improved Large Me; Rappel; Lean Gossip: Big Gains From Small Talk; Gossipsub-v1.1 Evaluation Report; Evaluating GossipSub for Data Availability Samplin
Example papers: 2019-araujo-communication-causal, 2019-vyzovitis-gossipsub-v01, 2020-leastauthority-gossipsub-audit, 2020-vyzovitis-gossipsub-v11-evaluation, 2022-taheri-spam-protected-gossip, 2025-farooq-staggering

## Secure Messaging Ratchets and Protocols  (229 nodes)
This cluster covers the Double Ratchet and related secure messaging protocols, their cryptographic components, and formal verification or analysis of messenger implementations.
Key nodes: Double Ratchet; From Specs to Apps: Verifying and Monitoring Model; Three Lessons From Threema: Analysis of a Secure M; Noise; WhatsApp Web; Wire Security Whitepaper; SimpleX Channels: overview and design; libsignal; SimpleX Channels; Advanced cryptographic ratcheting
Example papers: 2013-marlinspike-ratcheting, 2017-kobeissi-verification, 2018-jaeger-optimal-channel, 2021-guidi-libp2p-bitcoin, 2021-wire-securitywhitepaper, 2022-vac-waku2-x3dh-spec

## Asynchronous Messaging Key Agreement  (225 nodes)
The cluster covers X3DH and PQXDH session establishment, cryptographic key schedules and security assumptions, and analyses of attacks and protocols for secure asynchronous messaging.
Key nodes: X3DH; PQXDH; Domain Separation; gapDH; On Ends-to-Ends Encryption: Asynchronous Group Mes; Key confusion attack; The Double Ratchet: Security Notions, Proofs, and ; Mallory-in-the-middle attack; OW-CCA security; Curve DH key schedule
Example papers: 2016-cohngordon-signal, 2016-signal-double-ratchet-spec, 2017-cohngordon-art, 2018-alwen-double-ratchet, 2022-barnes-rfc9180, 2022-trailofbits-simplex-audit

## MLS Group State Attacks  (221 nodes)
This cluster concerns MLS and the insider or outsider attacks, including double-join attacks, that can arise from unsynchronized group state.
Key nodes: MLS; Insider and outsider attacks
Example papers: 2017-cohngordon-art, 2025-hashimoto-mls-app-auth

## Network Traffic Analysis and Anonymity  (209 nodes)
The cluster covers attacks that infer identities or encrypted content from traffic patterns and metadata, alongside network-layer systems designed to resist traffic analysis.
Key nodes: Traffic Analysis; TARANET: Traffic-Analysis Resistant Anonymity at t; Software Defined Networks; Dovetail; Eavesdropping; Encrypted Content Inference; Enigma; LAP; Exposed Communication Metadata; W3C Web Authentication API
Example papers: 2009-danezis-sphinx, 2017-barman-prifi, 2017-halpin-nextleap, 2018-chen-taranet, 2021-diaz-nym, iog-kachina-foundations-of-private-smart-contracts

## Privacy-Preserving P2P Social Networks  (201 nodes)
The cluster covers decentralized social networking and publishing systems that use DHTs, overlays, gossip, and cryptographic or anonymous communication to support privacy and censorship resistance.
Key nodes: Distributed Hash Table; Peer-to-Peer-Based Social Networks: A Comprehensiv; Do you feel a chill? Using PIR against chilling ef; LotusNet; Veilid; Want to scale in centralized systems? Think P2P; LifeSocial.KOM / LibreSocial; Cachet; LLARP; A branch hash function as a method of message sync
Example papers: 2011-chen-scaling-construction, 2012-ferretti-publish-subscribe, 2013-boutet-decentralizing, 2013-fukui-two-tier, 2013-leone-content, 2013-morales-supportscientific

## Gossip Network Attacks and Resilience  (198 nodes)
The cluster covers gossip and peer-to-peer network behavior, including censorship-resistant access, topology inference, protocol verification, and attacks on message forwarding.
Key nodes: Eclipse Attack; MoneyMorph: Censorship Resistant Rendezvous using ; Simple Payment Verification; Ouroboros Genesis; Timing Analysis for Inferring the Topology of the ; GossipSub v1.1 specification; Verification of GossipSub in ACL2s
Example papers: 2011-pace-gossiping, 2016-neudecker-timing, 2020-gossipsub-v11-spec, 2020-minaei-moneymorph, 2023-kumar-gossipsub-acl2s, iog-ouroboros-crypsinous-privacy-preserving-proof-of-stake

## Waku and Whisper Messaging Protocols  (190 nodes)
This cluster covers Waku and Whisper as decentralized messaging transports, including Waku’s relay network, discovery, filtering, light publishing, message storage, and secure transport.
Key nodes: Waku; Whisper; ADVERSARIAL-MODELS: Waku v2 adversarial models and; The Waku Network as Infrastructure for dApps; 6/WAKU1 (Waku v1, Whisper-derived); 14/WAKU2-MESSAGE; DISC-NG: Robust Service Discovery in the Ethereum ; Status 3/WHISPER-USAGE (v0.3); Waku Filter; Waku Lightpush
Example papers: 2017-eip-627-whisper, 2018-status-whisper-mailserver-spec, 2018-status-whisper-usage-spec, 2019-status-secure-transport-spec, 2019-vac-waku-mail-spec, 2019-vac-waku1-spec

## Post-Compromise Security in Group Messaging  (187 nodes)
The cluster covers post-compromise recovery and forward security in secure messaging, including ratchets, concurrent group key agreement, and MLS propose-and-commit updates.
Key nodes: Post-Compromise Security; CoCoA: Concurrent Continuous Group Key Agreement; Modular Design of Secure Group Messaging Protocols; Propose and Commit; Post-Compromise Security; Post-compromise forward security (PCFS); Ratchet; Efficient Ratcheting: Almost-Optimal Guarantees fo; Forward Security; Predictable RNG risk
Example papers: 2013-marlinspike-ratcheting, 2016-cohngordon-pcs, 2016-cohngordon-signal, 2018-jost-efficient-ratcheting, 2022-alwen-cocoa, iog-modular-design-of-secure-group-messaging-protocols-and-the-s

## Signal Protocol Security Analysis  (186 nodes)
This cluster covers formal security proofs for the Signal Protocol, including key indistinguishability, session-key reductions, security assumptions, and related attacks and mechanisms.
Key nodes: Signal Protocol; A Formal Security Analysis of the Signal Messaging; Key Indistinguishability; Off-the-Record Communication, or, Why Not To Use P; Session-key game hops; Time-of-check to time-of-use; Reduction loss; Signal core security result; Out-of-order message-key storage; Freshness and cleanness conditions
Example papers: 2004-borisov-otr, 2016-cohngordon-signal, 2016-whatsapp-security-whitepaper, 2022-albrecht-bridgefy-again

## Sybil-Resistant Anonymous Messaging  (185 nodes)
This cluster covers Sybil threats and defenses in peer sampling and anonymous communication, alongside privacy-preserving messaging, rumor-source obfuscation, and decentralized message delivery.
Key nodes: Sybil Attack; Honeybee: Byzantine Tolerant Decentralized Peer Sa; A Note on Notes: Towards Scalable Anonymous Paymen; Witnet; Accumulator; Lightweight Practical Private One-Way Anonymous Me; Spy vs. Spy: Rumor Source Obfuscation; XIP-49: Decentralized backend for MLS messages; ShadowWalker; Tor proposal 292: Mesh-based vanguards
Example papers: 2002-douceur-sybil, 2015-basu-lightweight, 2015-fanti-spyvsspy, 2019-tor-prop292-vanguards, 2021-pasdar-oracle-design-patterns, 2023-tor-prop333-vanguardslite

## Tor Anonymity Network  (185 nodes)
The cluster concerns Tor’s anonymous communication architecture, directory and relay infrastructure, privacy protections, attacks, measurement methods, and quantum-resilient messaging.
Key nodes: Tor; Tor Directory Authorities; k-fingerprinting: a Robust Scalable Website Finger; Quiet: encrypted p2p team chat over Tor (README); Tor call-tracing result; HisTorϵ; Harvest now, decrypt later; Tor Relay Count; Quantum risk to RSA and ECC; Stateless TLS connections
Example papers: 2010-corrigangibbs-dissent, 2014-winter-spoiledonions, 2015-leblond-herd, 2016-hayes-kfingerprinting, 2018-mani-tor-usage-privacy-preserving, 2018-tor-vanguards-spec

## Forward Secrecy in Group Messaging  (179 nodes)
This cluster covers forward secrecy and key-update mechanisms for private group messaging, including secure deletion, associated-data encryption, and transport protections.
Key nodes: Forward Secrecy; The Key Lattice Framework for Concurrent Group Mes; Off The Record (OTR); PKEAD; Secure deletion; Bramble Transport Protocol (BTP), version 4; Message Layer Security
Example papers: 2004-borisov-otr, 2016-briar-btp, 2016-signal-double-ratchet-spec, 2022-cong-key-lattice, 2025-wallez-thesis

## Mixnet Latency and Cost  (173 nodes)
This cluster covers mixnet routing and broadcast designs, their latency and ciphertext-size costs, and techniques for private collaboration over mixnets.
Key nodes: Mixnet; Are we collaborative yet? A Usability Perspective ; Broadcast Anonymous Routing (BAR); Mixnet latency cost; Mixnet ciphertext-size cost; Mixnet Cost and Latency Concern; Private Set Cardinality; YATA
Example papers: 2005-camenisch-onion-formal, 2017-halpin-nextleap, 2021-diaz-nym, 2021-javani-aot, 2022-shirali-dcnetsurvey, 2026-davitt-mixnetusability

## Private Information Retrieval  (173 nodes)
The cluster covers private database and pub/sub retrieval, including computational and client-preprocessing schemes, privacy trade-offs, and related confidentiality protections.
Key nodes: Private Information Retrieval; Communication-Computation Trade-offs in PIR; XPIR: Private Information Retrieval for Everyone; Single Pass Client-Preprocessing Private Informati; MIR; Popcorn; Symmetric PIR (SPIR); Cryptography from Anonymity; Enhanced Functionality and Confidentiality for Dat; Cwtch Security Handbook: Cwtch Server
Example papers: 1998-chor-pir, 2006-ishai-cryptography-from-anonymity, 2016-aguilarmelchor-xpir, 2016-crescenzo-enhanced, 2019-ali-pircommcomp, 2021-cwtch-server-component

## TreeKEM and MLS Group Key Management  (172 nodes)
The cluster covers TreeKEM and MLS tree-based mechanisms for managing asynchronous group keys, including ratchet trees, concurrent updates, and their security and efficiency analysis.
Key nodes: TreeKEM; Continuous Group-Key Agreement: Concurrent Updates; Security Analysis and Improvements for the IETF ML; TreeKEM: Asynchronous Decentralized Key Management; Ratchet Tree; Pseudorandom generator; TreeKEM Key Graph; On the Worst-Case Inefficiency of CGKA; Asynchronous Ratcheting Trees (ART); CPA-Secure Public-Key Encryption
Example papers: 2018-bhargavan-treekem, 2021-hashimoto-chained-cmpke, 2022-bienstock-cgka-worst-case, 2022-newman-spectrum, 2025-auerbach-cgka-no-pruning, iog-security-analysis-and-improvements-for-the-ietf-mls-standard

## Topic-Based Pub/Sub Overlay Design  (162 nodes)
The cluster covers algorithms and topology techniques for constructing and optimizing overlays that route and disseminate topic-based or content-based publish/subscribe messages.
Key nodes: Topic-Connected Overlay; Efficient tree-based content-based routing schemes; Comparative Evaluation of Dataflow Component Selec; On the Approximability of Minimum Topic Connected ; Techniques for Overlay Design of Content-based Pub; Content-based Dynaic Routing in Structured Overlay; Incremental Topology Transformation for Publish/Su; Low-diameter topic-based pub/sub overlay network c; A Generalized Algorithm for Publish/Subscribe Over; Distributed Ranked Data Dissemination in Social Ne
Example papers: 2011-hosoda-approximability-minimum, 2011-tajuddin-techniques, 2012-chen-generalized-algorithm, 2013-zhang-distributed-ranked, 2014-chen-algorithms-divide, 2015-shafique-content-dynaic

## Differentially Private Messaging  (161 nodes)
The cluster centers on scalable metadata-private messaging systems that use differential privacy, cover traffic, oblivious access, and distributed shuffling to reduce communication cost and latency.
Key nodes: Karaoke; Stadium; Myco: Unlocking Polylogarithmic Accesses in Metada; Karaoke: Distributed Private Messaging Immune to P; Groove; Poisson distribution; Path ORAM; Automerge
Example papers: 2017-kwon-atom, 2018-lazar-karaoke, 2018-wust-zlite, 2023-sasy-sokmetadata, 2025-kaviani-myco, 2026-davitt-mixnetusability

## Proof-of-Work Decentralized Messaging  (155 nodes)
This cluster covers Dpush and Dmail, which use proof of work, reputation, and a Kademlia-based DHT to support spam-resistant unsolicited messaging with encrypted delivery.
Key nodes: Proof of Work; Dpush: A scalable decentralized spam resistant uns; Dpush; MORPHiS; Dmail; Reputation system; TargetedBlock; Proofs of Useful Work (uPoW); Updateable Key; Proof of Work can Work
Example papers: 2002-back-hashcash, 2006-liu-pow, 2015-maloney-dpush, 2017-ball-usefulwork

## Topic-Connected Pub/Sub Overlays  (152 nodes)
The cluster covers publish/subscribe systems that organize peers into topic-based or spatial overlays to support scalable, resilient event dissemination and dynamic subscriptions.
Key nodes: Topic-Based Pub/Sub; C-DAX; Brief announcement: constructing fault-tolerant ov; Self-organizing spatial publish subscribe; Flexub: Dynamic Subscriptions for Publish/Subscrib; Pogo, a Middleware for Mobile Phone Sensing; A Trustworthy and Resilient Event Broker for Monit; Identity Management and Integrity Protection in Pu; Supporting End-to-end Scalability and Real-time Ev; A DDS/SDN Based Communication System for Efficient
Example papers: 2011-chen-scaling-construction, 2011-hu-self-organizing, 2012-bainomugisha-flexubdynamic, 2012-brouwers-pogomiddleware, 2012-kreutz-trustworthyresilient, 2013-chen-brief-announcement

## DHT-Based Publish-Subscribe  (149 nodes)
The cluster covers Kademlia and IPFS routing as foundations for decentralized content-based pub-sub, alongside delivery protocols and data-availability techniques.
Key nodes: Kademlia; SmartPubSub: Content-based Pub-Sub on IPFS; ScoutSubs; Scalability limitations of Kademlia DHTs when enab; Data Availability Sampling; FastDelivery; SmartPubSub; The Internals of Veilid: A New Distributed Applica; Erasure Coding; Hermes
Example papers: 2011-timpanaro-i2p, 2022-agostinho-smartpubsub, 2023-veilid-launch-slides, 2024-cortes-das-kademlia

## Content-Based Publish/Subscribe Routing  (148 nodes)
This cluster covers subscription matching and covering techniques, adaptive transitions, and overlay-based forwarding for content-based publish/subscribe systems.
Key nodes: Content-Based Pub/Sub; Parallel Search Trees; Opportunistic Multipath Forwarding in Content-Base; Approximate covering detection among content-based; Towards an Adaptive Publish/Subscribe Approach Sup; A Framework for Publish/Subscribe Protocol Transit; Content Based Publish / Subscribe systems for AANE; Secret Forwarding of Events over Distributed Publi; An Autonomous and Dynamic Coordination and Discove; Subscription Covering for Relevance-Based Filterin
Example papers: 2011-carzaniga-contentbased, 2012-kazemzadeh-opportunistic, 2012-lahyani-manetself, 2012-shen-approximate, 2013-richerzhagen-adaptivepublish, 2013-zhang-sdnlike

## Nym Mixnet Traffic Correlation  (147 nodes)
The cluster covers Nym’s privacy infrastructure and incentive mechanisms alongside flow-matching and timing-correlation attacks that test mixnet anonymity.
Key nodes: Nym; The Nym Network: The Next Generation of Privacy In; Analysis and Attacks on the Reputation System of N; DeepCoffea; Flow matching; MixFlow: Assessing Mixnets Anonymity with Contrast; DeepCorr; Tendermint; MixMatch: Flow Matching for Mixnet Traffic; Global Network Adversary
Example papers: 2018-ramachandran-trinity, 2020-bahramali-practical, 2021-diaz-nym, 2023-attarian-mixflow, 2024-oldenburg-mixmatch, 2025-yuan-earlymfc

## Metadata-Private Messaging  (141 nodes)
Systems and security definitions for hiding message content and communication metadata, including sender-recipient relationships, over fully untrusted infrastructure.
Key nodes: Pung; Addra; Pung: Unobservable Communication over Fully Untrus; Addra: Metadata-private voice communication over f; Relationship Unobservability; Formal Security Definition of Metadata-Private Mes; TEEMS: A Trusted Execution Environment based Metad; Fully untrusted infrastructure; Subcube batch codes; Content privacy
Example papers: 2016-angel-pung-1, 2021-ahmad-addra, 2022-zhang-formal-def-metadata-private-messaging, 2025-teems

## Privacy Coin Anonymity and Viewing Keys  (139 nodes)
The cluster covers privacy coins such as Zcash, Monero, and Firo, their anonymity mechanisms and viewing keys, and analyses of practical deanonymization and network attacks.
Key nodes: Zcash; Monero; Privacy Coins Under Viewing Key Compromise; Firo; Deanonymizing Monero Transactions in Tor Network; Viewing Key; An Empirical Analysis of Anonymity in Zcash; Lelantus Spark; UTXO Model; Eclipse Attacks on Monero's Peer-to-Peer Network
Example papers: 2016-hopwood-zcash-protocol-spec, 2018-grigg-zip307-light-client, 2018-kappos-zcash-anonymity, 2018-liu-keyinsulatedstealth, 2018-zcash-zip307, 2018-zip302-memo-format

## Sphinx Mix-Network Packet Formats  (138 nodes)
The cluster covers Sphinx cryptographic packets and variants for anonymized mix-network messaging, including multi-recipient delivery, replay detection, and active-adversary resistance.
Key nodes: Sphinx; OmniSphinx: Active Mix Networks; PolySphinx; Sphinx Packet Replay Detection (Katzenpost specifi; AE-Sphinx; MultiSphinx; Katzenpost Sphinx Cryptographic Packet Format Spec
Example papers: 2009-danezis-sphinx, 2026-coijanovic-omnisphinx, spec-katzenpost-packetreplay, spec-katzenpost-sphinx

## Zero-Knowledge Credential Protocols  (138 nodes)
The cluster covers zero-knowledge proofs, efficient signature protocols for committed messages, and verifiable encryption for linking encrypted secret delivery with data.
Key nodes: Zero-Knowledge Proof; Signatures with efficient protocols (SEP); Verifiable encryption
Example papers: 2010-pfitzmann-terminology, 2021-duguey-thesis, 2024-argo-pq-signatures-privacy

## Dining Cryptographer Networks  (131 nodes)
The cluster covers DC-net anonymity, including k-anonymous messaging protocols, silent-round schemes, partitioned deployments, and cryptographic PRNG-generated pads.
Key nodes: DC-net; Arbitrary Length k-Anonymous Dining-Cryptographers; Anonycaster; von Ahn k-anonymous message transmission protocol; Herbivore; Cryptographic PRNG
Example papers: 2003-goel-herbivore, 2013-corrigangibbs-verdict, 2015-unger-sok-securemessaging-tr, 2020-das-comprehensivetrilemma, 2021-modinger-k-anonymous-dc

## Bloom Filter Interest Dissemination  (128 nodes)
The cluster covers Bloom filters and their false-positive behavior in decentralized systems for matching interests, discovering peers, and filtering or disseminating relevant data.
Key nodes: Bloom Filter; Decentralizing news personalization systems; Bloom Filter False Positive; False Positive Rate Formula; BIP 37: Connection Bloom Filtering; BIP 157: Client Side Block Filtering; Enhanced SDP-dynamic bloom filters for a DDS node ; EFPIX: An Encrypted Flood Protocol for Metadata-Re; GOSSPLE; P3Q
Example papers: 2005-ostrovsky-streamingsearch, 2011-sanchezmonedero-ddsbloom, 2012-bip37-bloomfilter, 2013-boutet-decentralizing, 2013-lehn-distributed, 2017-bip157-clientfilters

## Anonymous Credential Systems  (127 nodes)
The cluster covers privacy-preserving credentials and authentication primitives, including group signatures, zero-knowledge proofs, DAA, and ledger-supported identity systems.
Key nodes: Anonymous Credentials; Privacy-Preserving Authentication: Theory vs. Prac; Commit-Transferrable Signature (CTS); EPID group key; Non-interactive zero-knowledge proof of knowledge; DAA; Distributed Ledger Technology; Service Provider; Single Sign-On
Example papers: 2016-cohngordon-signal, 2017-kim-sgxtor, 2021-diaz-nym, 2023-lai-commit-transferrable-sig, 2024-argo-pq-signatures-privacy, 2025-slamanig-privacy-auth

## Loopix Mixnets and Latency Optimization  (126 nodes)
The cluster covers Loopix-style mixnets, their anonymity assumptions and mixing mechanisms, and routing and latency optimizations that trade delay against anonymity.
Key nodes: Loopix; Global passive adversary; The Loopix Anonymity System; Blending Different Latency Traffic With Beta Mixin; LARMix: Latency-Aware Routing in Mix Networks; LAMP: Lightweight Approaches for Latency Minimizat; OptiMix: Scalable and Distributed Approaches for L; (n−1) attack; Stop-and-go mixing; Mixnode adversary
Example papers: 2016-hayes-tasp, 2017-das-trilemma, 2017-piotrowska-loopix, 2024-benguirat-betamixing, 2024-rahimi-larmix, 2025-rahimi-lamp

## TreeKEM External Operations Security  (122 nodes)
The cluster covers security analysis of MLS TreeKEM external operations and ETK variants that use external self-add and resumption PSKs.
Key nodes: ETK: External-Operations TreeKEM and the Security ; ETK; ETKPSK
Example papers: 2025-cremers-etk

## Traceable Mixnet Cryptography  (117 nodes)
The cluster covers a traceable mixnet and the threshold encryption, proof, signature, and hardness-assumption primitives used to support its implementation and security.
Key nodes: Traceable mixnets; Traceable mixnets; Fiat-Shamir heuristic; BN254 curve; Threshold encryption; Boneh–Boyen (BB) signatures; Distributed proof of knowledge; Threshold Paillier; DCR assumption; Decisional composite residuosity
Example papers: 2018-unger-deniable, 2023-agrawal-traceablemixnets

## Zero-Knowledge Anonymous Payments  (117 nodes)
This cluster covers zk-SNARK-based anonymous payment systems and the cryptographic primitives and security models used to protect payment details and verify spends.
Key nodes: zk-SNARK; Zerocash; Zerocash: Decentralized Anonymous Payments from Bi; Zerocoin; Key-private encryption; Universal Composition (UC) model; Collision-resistant hashing
Example papers: 2014-bensasson-zerocash, iog-kachina-foundations-of-private-smart-contracts

## Distributed MQTT Broker Overlays  (114 nodes)
The cluster covers distributed publish/subscribe broker architectures, including MQTT federation, overlay coordination, and methods for scaling event delivery across edge, cloud, and mobile settings.
Key nodes: MQTT; FTP; Queueing Network Modeling Patterns for Reliable an; ADPS (Asynchronous Distributed Publish Subscribe); Virtual ring method; Weighted Overlay Design for Topic-Based Publish/Su; Messaging with Purpose Limitation –Privacy-Complia; Cloud-edge MQTT messaging for latency mitigation a; A Hot-topic based Distribution and Notification of; The control mechanism of distributed MQTT brokers 
Example papers: 2011-davis-presencearchitecture, 2013-morales-hottopic, 2015-chen-weighted-overlay, 2018-bouloukakis-queueingnetwork, 2019-banno-interworking-layer, 2021-wolf-messaging

## Traffic-Analysis-Resistant Messaging  (112 nodes)
The cluster covers private messaging and gossip protocols that use cover traffic or differential privacy to limit traffic analysis, alongside work measuring anonymity fingerprints in onion services.
Key nodes: Cover Traffic; Vuvuzela; Vuvuzela: Scalable Private Messaging Resistant to ; How Unique is Your .onion? An Analysis of the Fing; Quantifying Differential Privacy of Gossip Protoco
Example papers: 2013-wolinsky-hang, 2015-vandenhooff-vuvuzela, 2017-overdorf-onion, 2019-huang-quantifying

## Metadata Privacy and Deanonymization  (112 nodes)
This cluster examines how communication metadata, IP addresses, and gossip timing can reveal who is talking or identify network participants, with consequences for private messaging and blockchain security.
Key nodes: Metadata Privacy; Deanonymizing Ethereum Validators: The P2P Network; IP Address Exposure; Network ossification; Time-bandit attack; What's a Little Leakage Between Friends?
Example papers: 2004-borisov-otr, 2018-angel-little-leakage, 2021-diaz-nym, 2024-heimbach-deanon, 2025-gunther-hybrid-obfuscated-kex

## Verdict Anonymous Messaging  (109 nodes)
The cluster centers on Verdict’s proactively verifiable DC-net system for anonymous group messaging, its cryptographic building blocks and defenses, and related work on accountable broadcast and decentralized coordination.
Key nodes: Verdict; Transparency Dictionaries with Succinct Proofs of ; Proactively Accountable Anonymous Messaging in Ver; ElGamal encryption; SNARK; Byzantine Fault Tolerance; DC-net jamming attack; Hash chains; Indexed Merkle trees; Append-only property
Example papers: 2013-corrigangibbs-verdict, 2018-poettering-asynchronous-rke, 2019-venkatapathy-decentralized-context-broker, 2022-tzialla-transparencydictionaries, 2024-cho-algebraicbroadcast

## Threshold-Based Group Key Quarantine  (109 nodes)
The cluster covers secret sharing and group key management that quarantine inactive members, alongside anonymity tradeoffs in coordinated communication and centralized security management.
Key nodes: Quarantined-TreeKEM (QTK); Secret Sharing; Anonymity Trilemma: Beyond Mix-Nets; Centralized Security Manager
Example papers: 2013-yoon-adaptation-techniques, 2020-das-beyond-mixnets, 2023-chevalier-quarantined-treekem

## Formal Verification of Secure Messaging Protocols  (109 nodes)
This cluster covers symbolic and machine-checked analyses of secure group messaging, key encapsulation, and related protocols, including MLS, Matrix, iMessage PQ3, and SPDM.
Key nodes: A Verification Framework for Secure Group Messagin; ProVerif; TreeKEM: A Modular Machine-Checked Symbolic Securi; Tamarin; Keeping Up with the KEMs: Stronger Security Notion; DY*; TreeSync; Dolev–Yao symbolic model; Comparse; PQ-SPDM
Example papers: 2015-decouchant-collusions, 2023-auerbach-pcs-cost-concurrent, 2023-beguinet-tamarin-pqsignal, 2023-cremers-keeping-up-kems, 2024-bhargavan-pqxdh, 2024-linker-imessage-pq3

## Accountable Anonymous DC-Net Messaging  (108 nodes)
This cluster covers Dissent and related dining-cryptographer networks, combining anonymous group messaging with verifiable accountability, privacy against collusion, and designs for scaling to larger groups.
Key nodes: Dissent; A Survey on Anonymous Communication Systems with a; Collusions and Privacy in Rational-Resilient Gossi; Dissent: Accountable Anonymous Group Messaging; PeerReview; TrInc; Attested Append-Only Memory; 3P3; Accountable Virtual Machines; Dissent in Numbers
Example papers: 2010-corrigangibbs-dissent, 2015-decouchant-collusions, 2022-shirali-dcnetsurvey

## Anonymity Set and Fingerprinting  (108 nodes)
This cluster concerns anonymity sets in communication systems, including website fingerprinting attacks, provable defenses, and long-term intersection risks.
Key nodes: Anonymity Set; Effective Attacks and Provable Defenses for Websit; Chaum DC-net security analysis; Long-term intersection attack
Example papers: 2010-corrigangibbs-dissent, 2013-corrigangibbs-verdict, 2014-wang-effectivewf

## Messaging Protocol Security Analysis  (108 nodes)
The cluster covers formal and computational security analysis of messaging protocols, including key derivation, authentication, hybrid key agreement, group messaging, and metadata privacy.
Key nodes: HKDF; EUF-CMA; PQ3; Formal Analysis of Multi-Device Group Messaging in; How to Hide MetaData in MLS-Like Secure Group Mess; Security analysis of the iMessage PQ3 protocol; HMAC-SHA256; Encrypted attachments; Triple Diffie–Hellman; CPA security
Example papers: 2014-syta-dissentanalysis, 2016-matrix-megolm-spec, 2016-matrix-olm-spec, 2017-pybitmessage-repo-protocol-docs, 2018-giacon-kem-combiners, 2021-madathil-privatesignaling

## TreeKEM Group Key Management  (108 nodes)
This cluster concerns TreeKEM and related administered group key agreement protocols, including security assumptions and efficiency improvements for managing membership and key updates.
Key nodes: TreeKEM; Security and Efficiency of Secure Group Messaging ; Tainted TreeKEM; Partially active adversary; SUMAC
Example papers: 2020-bienstock-group-ratcheting-concurrency, 2025-lebrun-thesis

## Decentralized Data and Contract Systems  (107 nodes)
The cluster covers decentralized storage and social publishing, secure gossip-based messaging, smart contracts and oracles, and security attacks on their data and event flows.
Key nodes: Smart Contract; IPFS; Navigating Decentralized Online Social Networks: A; Total Eclipse of the Heart - Disrupting the InterP; NOISE-X3DH-DOUBLE-RATCHET; BREPubSub: A Secure Publish-Subscribe Model using ; Blockchain Oracle; ASTRAEA; Public-key peer identity; Re-entrancy attack
Example papers: 2018-ramachandran-trinity, 2020-albreiki-blockchain-oracles, 2022-prunster-ipfseclipse, 2023-pham-brepubsub, 2024-vac-noise-x3dh-double-ratchet-spec, 2025-jeong-dosn-overview

## Post-Quantum KEM Ratchets  (107 nodes)
This cluster covers ML-KEM and its use in the Sparse Post-Quantum Ratchet and Braid Protocol, alongside benchmark results for Kyber operations.
Key nodes: ML-KEM; Signal Protocol and Post-Quantum Ratchets; The ML-KEM Braid Protocol; KEM benchmark results
Example papers: 2016-signal-double-ratchet-spec, 2025-berger-pq-tor, 2025-connell-spqr, 2025-signal-mlkem-braid-spec

## Private Bulletin Board Messaging  (106 nodes)
The cluster covers anonymous messaging systems that use PIR and distributed point functions, along with their metadata privacy, efficiency, and server-side attack defenses.
Key nodes: Riposte; Express; SoK: Metadata-Protecting Communication Systems; Express: Lowering the Cost of Metadata-hiding Comm; Private Information Retrieval; Sabre; SealPIR; RUS; SUBS; Anonymity-set manipulation attack
Example papers: 2015-corrigangibbs-riposte, 2018-ando-practical-onion-routing, 2019-ali-pircommcomp, 2020-abraham-blinder, 2020-kuhn-sokperformance, 2021-eskandarian-express

## Metadata-Private Anonymous Broadcast  (106 nodes)
The cluster covers anonymous broadcast and messaging systems that use distributed point functions and oblivious memory, including access control, auditing, and bandwidth-efficient private writes.
Key nodes: Distributed Point Function; Spectrum; Spectrum: High-bandwidth Anonymous Broadcast; Remise: Authorized Anonymous Communication Systems; Remise; Riposte: An Anonymous Messaging System Handling Mi; BlameGame; DORAM; Anonymous access control; Audit attack
Example papers: 2015-corrigangibbs-riposte, 2022-newman-spectrum, 2026-ravi-remise

## Oblivious Message Retrieval  (104 nodes)
This cluster covers oblivious message retrieval and PIR techniques used to discover and privately retrieve messages, including their role in anonymous messaging systems such as Kerblam.
Key nodes: Oblivious Message Retrieval; Kerblam; Kerblam: Anonymous Messaging System Protecting Bot; Trusted Execution Environment (TEE); PerfOMR: Oblivious Message Retrieval with Reduced ; Aztec documentation: private events, note discover; HomeRun; The Capacity of Private Information Retrieval
Example papers: 2016-sun-pircapacity, 2024-aztec-private-events-note-discovery, 2024-liu-perfomr, 2025-jia-kerblam

## Post-Quantum KEM Anonymity  (103 nodes)
This cluster covers QROM proofs and security properties for anonymity and chosen-ciphertext security of Kyber and other post-quantum KEMs, including their underlying assumptions and reductions.
Key nodes: Anonymity of NIST PQC Round 3 KEMs; Post-Quantum Anonymity of Kyber; Quantum random oracle model; IND-CCA security; NTRU assumption; IND-CPA security; SPR-CCA security; ANO-CCA security; SSMT-CCA security; U̸⊥
Example papers: 2017-bindel-transition-pki, 2017-chen-psihe, 2017-kwon-atom, 2017-polyakov-prepubsub, 2020-bellare-imessage-signcryption, 2022-grubbs-anonrobustpq

## Metadata-Private Anonymous Messaging  (102 nodes)
The cluster covers metadata-protecting communication and anonymous messaging systems, including private dialing, searchable bulletin boards, identity-based encryption, and accountable stealth signatures.
Key nodes: Alpenhorn; 2021-beck-fmd; Identity-Based Encryption (IBE); Alpenhorn: Bootstrapping Secure Communication with; Yodel: Strong Metadata Security for Voice Calls; Stealth and Beyond: Attribute-Driven Accountabilit; FMD2; Private Identity-based Bulletin Boards for Anonymo; Discrete log assumption; FracFMD
Example papers: 2004-boneh-peks, 2014-chase-algebraicmacs, 2015-nholambe-maintenancetopology, 2016-angel-pung-1, 2016-lazar-alpenhorn, 2016-onica-confidentialitypreserving

## Accountable Metadata-Private Messaging  (102 nodes)
This cluster covers asymmetric message franking and related cryptographic techniques for enabling abuse reporting and moderation in metadata-private messaging while preserving deniability and sender privacy.
Key nodes: Asymmetric Message Franking (AMF); Asymmetric Message Franking: Content Moderation fo; Better Security Proofs for X3DH and XHMQV; Gap Diffie-Hellman assumption; Discrete Logarithm (DL) assumption; Zero Knowledge; Provable Security for the Onion Routing and Mix Ne; Hecate: Abuse Reporting in Secure Messengers with ; Designated-verifier signatures; Knowledge of Exponents Assumption (KEA)
Example papers: 2012-libert-anonymousbe, 2013-corrigangibbs-verdict, 2019-tyagi-messagefranking, 2021-issa-hecate, 2024-scherer-sphinxproof, 2026-bao-x3dh-tight

## Lattice-Based Oblivious Retrieval  (102 nodes)
This cluster covers lattice-based encryption and SIS hardness used to protect clues in oblivious message retrieval, including Gaussian elimination to recover payloads from independent equations.
Key nodes: Oblivious Message Retrieval; PVW encryption; Short Integer Solution (SIS); Regev05 encryption; Gaussian elimination
Example papers: 2021-liu-omr

## Efficient Key Transparency Dictionaries  (101 nodes)
This cluster covers Aegon and related transparent dictionaries that use polynomial commitments and verifiable auditing to support scalable, privacy-preserving key transparency.
Key nodes: Aegon: Self-Auditable Key Transparency; Aegon; SEEMless; WhatsApp Key Transparency (AKD); KZH; Schwartz–Zippel Lemma; Verifiable Pseudorandom Function (VRF); IronDict; KZH-k; Server
Example papers: 2022-tzialla-transparencydictionaries, 2026-hafezi-aegon

## Authenticated Encryption and Message Authentication  (97 nodes)
The cluster covers authenticated-encryption constructions, MACs, and security analyses used to protect messaging and hybrid public-key encryption schemes.
Key nodes: Authenticated Encryption; HMAC; Message Franking via Committing Authenticated Encr; Encrypt-then-MAC; pSaber.PKEhy; Secure Messaging with Strong Compromise Resilience; zk-promises: Anonymous Moderation, Reputation, and; Carter-Wegman MAC; Encode-then-Encipher; GCM
Example papers: 2016-angel-pung-1, 2016-matrix-megolm-spec, 2017-grubbs-franking, 2022-cremers-pq-secure-messaging, 2022-grubbs-anonrobustpq, 2025-shih-zkpromises

## Messaging Contact Enumeration and Leakage  (96 nodes)
This cluster covers large-scale abuse of messaging contact discovery to enumerate accounts and reverse phone-number hashes, alongside traffic-size leakage in WhatsApp and Viber.
Key nodes: WhatsApp; All the Numbers are US: Large-scale Abuse of Conta; Enumeration attack; Hey there! You are using WhatsApp: Enumerating Thr; XMPP; Contact discovery; Telegram; Hash reversal attack; Device-Oriented Group Messaging (DOGM); Hashcat
Example papers: 2014-coull-imessage-privacy, 2018-johnsen-publishsubscribe, 2021-hagen-contact-discovery, 2025-albrecht-whatsapp-multidevice, 2026-gegenhuber-whatsapp-enumeration

## Leakage-Resilient Ratcheted Key Exchange  (95 nodes)
The cluster covers ratcheted key exchange protocols and security models, including partial-leakage resilience, key-updatable encapsulation, and attacks on key indistinguishability.
Key nodes: Random oracle simulation; Towards Leakage-Resilient Ratcheted Key Exchange; Sesquidirectional ratcheted key exchange (SRKE); URKE; Bounded leakage; Key-updatable key encapsulation mechanism (kuKEM); Bidirectionally ratcheted key exchange (BRKE); Leakage-resilient ratcheted key exchange; Key distinguishing attack; Birthday paradox
Example papers: 2001-bellare-keyprivacy, 2018-poettering-asynchronous-rke, 2021-ayavuz-lattice-pow, 2024-celi-keywordpir, 2025-collins-leakage-rke

## DHT-Based Publish-Subscribe Overlays  (94 nodes)
The cluster covers peer-to-peer publish-subscribe systems that use structured overlays such as Pastry and Skip Graph for topic routing, multicast, message ordering, and adaptation.
Key nodes: Scribe; A communication-efficient causal broadcast publish; Pastry DHT; Towards an ontology and DHT-based publish/subscrib; Designing Overlay Networks for Handling Exhaust Da; Dynamic Message Ordering for Topic-Based Publish/S; Bayeux protocol; Active adaptation; DRScribe; Magnet
Example papers: 2012-baldoni-dynamic-message, 2012-chaabane-ontology, 2012-setty-poldercast, 2013-rene-erreichen, 2015-banno-designing-overlay, 2015-costa-rayzit

## Blockchain and Pub/Sub Integration  (94 nodes)
The cluster covers blockchain-backed auditability and oracle event notifications alongside DDS and broker-based publish/subscribe systems, including reactive stream processing and SDN integration.
Key nodes: Ethereum; Eclipse Attacks on Bitcoin's Peer-to-Peer Network; Reactive stream processing for data-centric publis; DDS et SDN en symbioses pour les applications dyna; OPTIMASI PEMILIHAN CHILD BROKER(S) PADA MODEL KOMU; Foundational Oracle Patterns: Connecting Blockchai; EthIKS; Hawk trusted-manager setting; Reactive Programming
Example papers: 2015-hakiri-publishsubscribe, 2015-heilman-eclipse, 2015-khare-reactivestream, 2015-tegueu-ddssymbioses, 2017-hayun-optimasipemilihan, 2020-muhlberger-oracle-patterns

## Anonymous MLS Message Authentication  (93 nodes)
The cluster covers group-authenticated messaging for MLS, including anonymous signatures and blocklisting, token-based protocols, group key management, and their security and bandwidth properties.
Key nodes: Exploring How to Authenticate Application Messages; Quasar; Group signature; STARS; Unforgeability; COSMAC; COSMOS; Cryptographic Administration for Secure Group Mess; Upload, download, and total bandwidth; Tracing soundness
Example papers: 2011-mega-dissemination-decentralized, 2013-vansaberhagen-cryptonote, 2020-alonso-zerotomonero, 2022-balbas-a-cgka, 2025-hashimoto-mls-app-auth

## EROR Onion Routing Security  (93 nodes)
The cluster covers EROR’s efficient repliable onion packet construction, its integrated communication model, and security proofs against active payload tagging under a global adversary.
Key nodes: EROR; EROR: Efficient Repliable Onion Routing with Stron; Hybrid argument; Integrated system model; Anonymous Communication Network (ACN); DLR$-CPA security; Onionize; Payload tagging attack; FormOnion; Service model
Example papers: 2020-kuhn-sokperformance, 2024-klooss-eror, 2024-rial-outfox

## Hybrid Post-Quantum Messaging Cryptography  (93 nodes)
The cluster covers hybrid key agreement and KEM constructions combining X25519 with post-quantum cryptography, alongside their use in secure messaging and analyses of their security and anonymity.
Key nodes: X-Wing; X25519; Server-Aided Continuous Group Key Agreement; SHA3-256; Ilyazh-Web3E2E: A Post-Quantum Hybrid Protocol for; Nominal groups; X-Wing: The Hybrid KEM You’ve Been Looking For; Crypto Wars in Secure Messaging: Covert Channels i; SimpleX Agent Protocol; X-Wing: general-purpose hybrid post-quantum KEM (I
Example papers: 2013-tor-prop224-rendng, 2016-signal-x3dh-spec, 2018-tor-proposal-269-hybrid-handshake, 2021-alwen-server-aided-cgka, 2021-simplex-agent-protocol, 2023-kret-pqxdh-blog

## Latency-Aware Mixnet Routing  (92 nodes)
The cluster covers routing methods that reduce mixnet latency while managing the resulting costs to path randomness and message anonymity.
Key nodes: LARMix; MALARIA: Management of Low-Latency Routing Impact ; LOR; MORSE; CLAPS; CLAPS Mix; LASTor; Message anonymity
Example papers: 2024-rahimi-larmix, 2024-rahimi-larmixpp, 2025-rahimi-malaria

## Signal Prekey Handshake Cryptography  (92 nodes)
This cluster covers Signal’s X3DH and PQXDH prekey handshakes, their key derivation and agreement assumptions, post-quantum KEMs, and related cryptographic primitives.
Key nodes: Key Derivation Function (KDF); Bundled Authenticated Key Exchange: A Concrete Tre; PRF-ODH; PQXDH; Gandalf signature scheme; Key agreement; Key-less reproducibility; Kyber-1024; Gap-CDH; X3DH Key Agreement Protocol
Example papers: 2012-libert-anonymousbe, 2016-hopwood-zcash-protocol-spec, 2024-stebila-pq3-analysis, 2025-hashimoto-bundled-ake

## Lattice-Based Privacy Cryptography  (91 nodes)
The cluster covers lattice assumptions and constructions used for privacy, including anonymous credentials, signatures, commitments, and proofs.
Key nodes: Lattice-based Commit-Transferrable Signatures and ; Practical Post-Quantum Signatures for Privacy; M-LWE; M-SIS; Lattice-based cryptography; BDLOP Commitment; Cyclotomic field and ring; Galois group and fixed fields; Ideal lattice problems; M-ISIS
Example papers: 2023-abdennebi-latticepubsub, 2023-lai-commit-transferrable-sig, 2024-argo-pq-signatures-privacy

## Single-Server Private Information Retrieval  (91 nodes)
The cluster covers single-server PIR protocols and their cryptographic foundations, comparing SimplePIR and DoublePIR performance with Paillier- and LWE-based approaches and noting a key-recovery attack on a SealPIR configuration.
Key nodes: SimplePIR; Learning with Errors; DoublePIR; One Server for the Price of Two: Simple and Fast S; Paillier; Regev encryption; SealPIR
Example papers: 2016-aguilarmelchor-xpir, 2022-corrigangibbs-pirsublinearamortized, 2022-henzinger-simplepir

## Rumor Source Hiding  (90 nodes)
The cluster covers adaptive rumor-spreading protocols and graph-based methods for estimating or concealing the message source.
Key nodes: Adaptive diffusion; Hiding the Rumor Source; Flood-and-prune broadcast; Jordan centre; Galton-Watson process; Pólya’s urn process; Maximum-likelihood source estimator
Example papers: 2015-fanti-hidingrumor, 2021-modinger-statistical

## Respire Small-Record PIR  (89 nodes)
This cluster covers Respire’s compact, lattice-based PIR for retrieving small database records, including its query and response compression techniques and related PIR comparisons.
Key nodes: Respire; Respire: High-Rate PIR for Databases with Small Re; Batch Codes; Response Compression; GSW Encryption; Query Compression; Ring Switching; Homomorphic Selection; Gentry-Ramzan; Vectorized BatchPIR
Example papers: 2016-angel-pung-1, 2024-burton-respire

## MPC Anonymous Committed Broadcast  (88 nodes)
This cluster covers Blinder’s secure multiparty computation protocols for scalable, robust anonymous committed broadcast in synchronous networks.
Key nodes: Blinder; Blinder: Scalable, Robust Anonymous Committed Broa; Secure Multi-Party Computation; Anonymous committed broadcast; RPM; Synchronous network
Example papers: 2015-corrigangibbs-riposte, 2020-abraham-blinder, 2023-sasy-sokmetadata

## cMix Mix-Network Security  (88 nodes)
This cluster covers cMix and mix-cascade designs for unlinkable messaging, their efficiency and integrity checks, and attacks such as tagging, replay, and flooding.
Key nodes: cMix; Tagging attack; Replay attack; cMix: Mixing with Minimal Real-Time Asymmetric Cry; Key Agreement for Decentralized Secure Group Messa; Attacks on cMix - Some Small Overlooked Details; Randomized Integrity Checking (RPC); Untagging Tor: A Formal Treatment of Onion Encrypt; Bad Apple Attack; Mix cascade
Example papers: 2009-danezis-sphinx, 2016-galteland-cmixattacks, 2017-chaum-cmix, 2017-kim-sgxtor, 2018-degabriele-untagging-tor, 2018-shirazi-survey-routing-anon

## Zcash Shielded Cryptography  (88 nodes)
The cluster covers Zcash’s shielded transaction protocols and the cryptographic primitives, curves, proofs, and signatures used by Sapling, Orchard, and multi-asset pools.
Key nodes: Zcash Protocol Specification (living document, ver; Sapling; BLAKE2; Faerie Gold attack; Halo 2; Pallas; Strong unforgeability; Binding signature; Group hash; Jubjub
Example papers: 2016-hopwood-zcash-protocol-spec, 2022-namada-masp-spec

## Onion Routing and Mix Relays  (88 nodes)
The cluster covers onion-routed message delivery through layered relay processing, including anonymity assumptions and quantum-safe designs.
Key nodes: Onion Routing; 2018-rochet-dropping-on-the-edge; Mix-node; At least one honest relay; QSOR: Quantum-Safe Onion Routing; Session network documentation: Onion requests and 
Example papers: 2003-goel-herbivore, 2018-ando-practical-onion-routing, 2018-rochet-dropping-on-the-edge, 2020-tujner-qsor, 2024-klooss-eror, 2024-session-onion-requests-swarms

## Authenticated Key Encapsulation  (87 nodes)
The cluster covers authenticated key encapsulation mechanisms, their security assumptions and primitives, and their use in hybrid and post-quantum Sphinx designs.
Key nodes: Key encapsulation mechanism; Symmetric and Asymmetric Anonymous Authenticated K; Shadowfax: Hybrid Security and Deniability for AKE; NIKE; Symmetric encryption; PRF security; AKEM; AES-256-GCM; H2; Post Quantum Sphinx
Example papers: 2021-vac-waku2-payload-spec, 2022-cremers-pq-secure-messaging, 2023-stainton-pqsphinx, 2023-xmtp-xip42-consent, 2024-klooss-eror, 2025-gajland-shadowfax

## Blockchain Consensus and Network Security  (87 nodes)
This cluster covers blockchain consensus and oracle designs, peer-to-peer overlay measurement and attacks, and security risks from quantum adversaries and mining.
Key nodes: Proof of Stake; Trustworthy Blockchain Oracles: Review, Comparison; Securing Elliptic Curve Cryptocurrencies against Q; ethp2psim: Evaluating and deploying privacy-enhanc; Quantum adversary; Discovering the Ethereum2 P2P Network; Eclipse Attacks on Ethereum's Peer-to-Peer Network; On the insecurity of quantum Bitcoin mining; Decentralized Lightweight Detection of Eclipse Att; BASALT: A Rock-Solid Foundation for Epidemic Conse
Example papers: 2018-ramachandran-trinity, 2018-sattath-quantum-bitcoin-mining, 2020-alangot-eclipsedetection, 2020-albreiki-blockchain-oracles, 2020-cortes-eth2-p2p, 2021-auvolat-basalt

## Differential Privacy in Gossip  (87 nodes)
This cluster covers differential privacy guarantees for gossip source anonymity, their limits under dummy traffic, and related privacy frameworks and proof tools.
Key nodes: Differential Privacy; On the Inherent Anonymity of Gossiping; Who started this rumor? Quantifying the natural di; Do Dummies Pay Off? Limits of Dummy Traffic Protec; Data Processing Inequality; Pufferfish; Pufferfish framework; Rollback attack
Example papers: 2013-backes-anoa, 2014-oya-dummies, 2020-bellet-who, 2022-li-sok, 2023-guerraoui-inherent-anonymity-gossiping

## Public-Key Encryption Security  (85 nodes)
This cluster covers public-key encryption schemes and constructions, their confidentiality and robustness properties, and attacks and mechanisms relevant to KEMs and multirecipient encryption.
Key nodes: IND-CCA; IND-CPA security; Robustness; On The Insider Security of MLS; Implicit rejection; AES-CTR; Multi-recipient public-key encryption (MRPKE); KEM-DEM paradigm; Explicit rejection; Kyber-AKE
Example papers: 2012-libert-anonymousbe, 2017-bindel-transition-pki, 2017-bos-kyber, 2020-abraham-blinder, 2020-alwen-mls-insider, 2020-bellare-imessage-signcryption

## Waku Relay Rate Limiting  (85 nodes)
This cluster covers Waku v2 Relay and its Rate Limiting Nullifier mechanisms for economic spam resistance.
Key nodes: Rate-Limiting Nullifier; 10/WAKU2 (Waku v2 overview); 11/WAKU2-RELAY; RLN-V2 (Rate Limit Nullifier V2)
Example papers: 2020-vac-waku2-relay-spec, 2020-vac-waku2-spec, 2024-vac-rln-v2-spec

## Mobile Ad Hoc Publish/Subscribe Routing  (84 nodes)
This cluster covers routing and broadcast techniques for mobile ad hoc publish/subscribe networks, including source routing, multicast forwarding, and broadcast-storm effects.
Key nodes: Tree-based Power-aware Source Routing (TPSR); AODV; Content routing algorithms to support Publish/Subs; Broadcast Storm; PAMPA; Location Based Multicast (LBM); Towards a fully mobile publish/subscribe system; DSR; Received Signal Strength Indicator (RSSI)
Example papers: 2012-schnitzer-content-routing, 2016-royer-routagebase, 2021-amozarrain-fully

## Low-Latency Mixnet Topologies  (84 nodes)
This cluster covers low-latency mixnet designs, including node placement and methods for locating mixnodes in distributed networks.
Key nodes: OptiMix; Verloc
Example papers: 2025-rahimi-lamp, 2026-rahimi-optimix

## Anonymity Measurement and DC-Nets  (83 nodes)
The cluster covers anonymity metrics and threat models alongside DC-net systems and protocols designed to provide anonymity.
Key nodes: PriFi; PriFi: Low-Latency Anonymity for Organizational Ne; A Survey on Measuring Anonymity in Anonymous Commu; k-anonymity; TASP: Towards Anonymity Sets that Persist; Min-entropy; Buddies; Max-entropy; Rényi entropy; Arbitrary length k-anonymous
Example papers: 2016-hayes-tasp, 2017-barman-prifi, 2019-lu-survey, 2022-shirali-dcnetsurvey

## HQC Code-Based Cryptography  (83 nodes)
The cluster covers HQC’s code-based KEM security and implementation, including syndrome decoding, attacks, error-correcting codes, and its use in post-quantum ratcheted key exchange.
Key nodes: HQC; Hamming Quasi-Cyclic (HQC): specification, 22 Augu; Syndrome Decoding; The Tox Protocol Specification (TokTok); Perfect Forward Secrecy; IND-CCA2 security; Information Set Decoding; Reed-Muller code; Systematic Reed-Solomon code; RHQC: post-quantum ratcheted key exchange from cod
Example papers: 2013-tox-protocol-spec, 2022-xagawa-anonymitykems, 2025-dodis-triple-ratchet, 2025-hqc-specification, 2025-juaneda-rhqc

## Zenoh and Edge Middleware  (83 nodes)
This cluster covers Zenoh and related dataflow frameworks alongside DDS, Kafka, and SOME/IP middleware used for edge, robotics, and automotive communication.
Key nodes: Zenoh; FastDDS / FastRTPS; Kafka; Zenoh Flow; Cyclone DDS; vSomeIP; A Performance Study on the Throughput and Latency ; Zenoh-based Dataflow Framework for Autonomous Vehi; Automotive Middleware Performance: Comparison of F; ERDOS
Example papers: 2021-baldoni-zenohdataflow, 2022-berjon-eventmesh, 2023-liang-zenohperformance, 2024-chovet-performancecomparison, 2024-mehran-runtimeverification, 2025-kluner-zenohautomotive

## Freenet Anonymity and Intersection Attacks  (83 nodes)
This cluster concerns Freenet’s publishing modes and network behavior alongside anonymity notions and attacks that infer message origins from recurring network observations.
Key nodes: Intersection attack; Freenet; TASP; Measuring Freenet in the Wild: Censorship-resilien; On Privacy Notions in Anonymous Communication; Opennet; The Cost of Stability: Deanonymizing Onion Service; Darknet; On the Impossibility of Efficient Self-Stabilizati; FNPProbeRequest
Example papers: 2003-goel-herbivore, 2014-roos-measuring-freenet, 2015-roos-impossibility-self-stabilization, 2016-hayes-tasp, 2019-kuhn-privacynotions, 2026-constantinides-introcircuits

## Gossip-Based Pub-Sub Protocols  (83 nodes)
The cluster covers peer-to-peer publish/subscribe and gossip protocols, including their routing overlays, formal correctness and resilience analyses, and applications to replicated messaging.
Key nodes: Floodsub; Pulsarcast: Scalable, Reliable Pub-Sub over P2P Ne; A Formalization of the Correctness of the Floodsub; Hierarchical distributed hash table overlay; GossipSub: Attack-Resilient Message Propagation in; Farcaster Specifications (version 2023.11.15); Formal Model-Driven Analysis of Resilience of Goss; Well-Founded Simulation; Probabilistic Edge Multicast Routing for the XRP N
Example papers: 2011-sarela-bloomcasting, 2013-mega-social-overlays, 2020-vyzovitis-gossipsub, 2021-antunes-pulsarcast, 2022-kumar-gossipsub-formal, 2022-tumas-xrp-multicast

## Private User Discovery in Anonymity Networks  (81 nodes)
The cluster centers on Pudding’s anonymous user discovery and mutual authentication, with related reply-block, mixnet, deniability, and broadcast mechanisms.
Key nodes: Pudding; Pudding: Private User Discovery in Anonymity Netwo; Sigma protocol; Single-Use Reply Block; Hidden Services Protocol for Mixnets; Key-blinded signatures; Real-World Deniability in Messaging; DomainKeys Identified Mail (DKIM); Active flooding attack; Byzantine Reliable Broadcast
Example papers: 2014-chase-algebraicmacs, 2023-collins-real-deniability, 2023-kocaogullar-pudding, 2026-constantinides-hiddenservices

## Clustering for Mobile Publish-Subscribe Networks  (81 nodes)
The cluster covers node clustering and cluster-head election, maintenance, and multicast methods used to organize publish-subscribe and ad-hoc networks.
Key nodes: Routage basé sur le contenu dans les réseaux ad-ho; 2016-royer-content; CAPS; Using Machine Learning to Provide Reliable Differe; MOBIC; REDS (REconfigurable Dispatching System); LCC; LIC; Lowest ID Clustering (LIC); TCGM (Threshold Clustered Group Multicast)
Example papers: 2016-royer-content, 2016-royer-routagebase, 2019-shi-sdnmachine

## Threshold Selective-Disclosure Credentials  (81 nodes)
This cluster covers Coconut credentials, including threshold issuance, selective disclosure, unlinkable re-randomized use, and the cryptographic assumptions and primitives that support them.
Key nodes: Coconut; El Gamal; DDH assumption; Coconut: Threshold Issuance Selective Disclosure C; Pointcheval-Sanders signature; LRSW assumption; XDH assumption; PBKDF2; Selective disclosure credentials; Threshold issuance
Example papers: 2001-bellare-keyprivacy, 2012-libert-anonymousbe, 2019-sonnino-coconut, 2022-thambipillai-streamr-multicast-encryption

## I2P Network Measurement and Resilience  (81 nodes)
This cluster covers I2P’s garlic-routing architecture and studies measuring its network, censorship resistance, resilience, and anonymity risks.
Key nodes: I2P; An Empirical Study of the I2P Anonymity Network an; Monitoring the I2P network; Examining I2P Resilience: Effect of Centrality-bas; Garlic routing; Time will Tell: Large-scale De-anonymization of Hi; Garlic Routing
Example papers: 2011-timpanaro-i2p, 2018-hoang-i2p, 2021-diaz-nym, 2025-akanbi-i2pcentrality, 2025-wang-i2ptimewilltell

## Anonymity and Mixnet Optimization  (80 nodes)
This cluster covers anonymity guarantees and attacks in publish/subscribe and mix networks, including adaptive mixnet design, onion routing, and communication scheduling.
Key nodes: Anonymity Trilemma; Mitigating Intersection Attacks in Anonymous Micro; Studying the anonymity trilemma with a discrete-ev; Mixnet optimization methods; Footprint scheduling for Dining-Cryptographer netw; Gestion de la qualité de service des systèmes publ; Bruisable Onions: Anonymous Communication in the A; Exponentially Weighted Moving Average; k-mode clustering; A Rudimentary Model for Low-Latency Anonymous Comm
Example papers: 2012-matos-brisa-combining, 2012-naicken-finding, 2015-abdennadher-gestionqualite, 2015-krasnova-footprint, 2017-zheng-rudimentary-model, 2021-diaz-trilemmasimulator
