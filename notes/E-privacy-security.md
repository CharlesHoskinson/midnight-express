# Slice E-privacy-security: collection notes

Scope: privacy, confidentiality and security of decentralized pub/sub, 2011-2026.
Catalog: `catalog/E-privacy-security.jsonl` (124 records: 57 downloaded, 67 metadata_only, 0 not_found; 70 core, 54 adjacent).

## What this slice contains

Only papers that no other catalog already held were kept (matched on DOI, arXiv id and normalised title against every `catalog/*.jsonl` at the time of the last run). 148 candidate papers were already catalogued elsewhere (mostly in G-surveys-citations, PB2, PB7, C, D, F) and were dropped; their PDFs were not duplicated.

Main groups in the catalog (titles as in the catalog):

- Confidentiality-preserving content-based pub/sub: Thrifty privacy and its TDSC extension (prefiltering), Onica's thesis, key-update paper and kNN-based confidentiality, Ion et al. (confidentiality and access control), Broker-Based Private Matching, Cheng (untrusted platform), Yang/Jia (attribute-keyword search) and the 2019 proof-fix, PICADOR (proxy re-encryption), Denis (encrypted matching with data splitting), order-preserving-encryption and conjunctive-search schemes, Cui's key management, Crescenzo's database-search/pub-sub protocols, Mercier (Bloom-filter routing trade-offs), Tian (ubiquitous computing).
- Identity-based, attribute-based and revocation schemes: Thatmann (CP-ABE messaging patterns), Blazy (attribute-based topic security), Belguith, Zhao (CP-ABE revocation), Zhang (bilateral access control), Li (verifiable, hidden access policy), Yi (anonymous subscription with revocation), Malpure (pairing-based brokerless), REEDS.
- Trusted hardware and distributed security architectures: SCBR (SGX), MagikCube, LCM-RA, SecureStreams, DDS Security+ (TPM attestation), C-DAX security architecture, EventGuard, Munster's secret sharing in TEEs.
- Authorisation, identity and policy: Eyers/Bacon policy work (Shand, Singh), conflict detection for access control (Hein), Fongen, Xie (topic-centric), Pozo, Duan (smart-grid), Anantharaman, Galletta (proof-carrying payloads, 2026), DPS-IIoT (zero-knowledge-inspired), Decentralized Information-Flow Control for ROS 2, AVGuardian.
- DDS (brokerless) security: Murugesan (ABAC), Michaud (attacks), Wang (formal analysis), Lauser (formal and practical analysis), Wagner (TPM attestation), ROS 2 information-flow control.
- Attacks, DoS and spam: Aniello (overlay scan attack), Vivek (attacks on a privacy-preserving pub/sub system), Chifor (DoS in IoT pub/sub), Burglars' IoT Paradise, Collaborative RLN signaling (2026), RLN for sequencer admission (2026), SecureVent, Sybil-resistant peer discovery (AetherWeave).
- Byzantine membership: Basalt, AUPE, Mukam thesis.
- Anonymity, mixnet, DC-net and metadata-privacy building blocks that were not already held by PB1/PB2/PB7: Pung, anonymous microblogging and intersection attacks (Senftleben, Gaballah, Anix), Hang with Your Buddies, RAC, DiceMix, Bauer (DC-net for IoT), Rayzit, aDTN, DTN message exchange, Pudding, TrustMix, Multiparty Routing and Stopping Silent Sneaks (mixnets), traffic-analysis attacks on messengers, Metadata-private communication for the 99%, Metadata-private messaging without coordination (poster), Rangzen.
- Gossip and dissemination privacy: Who started this rumor, Quantifying DP of gossip protocols, Collusions and privacy in rational-resilient gossip, Statistical privacy-preserving message dissemination.
- Censorship resistance: Tithonus, MoneyMorph, PIR against chilling effects, Censorship-evident publishing.
- Surveys, SoKs and theses: SoK on privacy-preserving smart contracts, SoK on TEE-assisted confidential smart contracts, measuring anonymity in anonymous communication systems, a survey of DHT security techniques, theses by Onica, Klingler, Decouchant and Mukam, Munster's thesis.

The big survey and system papers of this area (Onica et al. survey, Uzunov, Esposito, PubSub-SGX, 2PPS, Cui's TDSC papers, Tariq's identity-based scheme, AnonPubSub, GossipSub and the Waku/RLN line) were found by this search too but are already catalogued by G, C, D and PB* and so do not appear here.

## Method and queries

All discovery used APIs that answered without a login and without any e-mail address. No git command was run, no paywall or bot wall was bypassed.

| Source | Use | Queries / notes |
|---|---|---|
| OpenAlex | initial search; later single-work lookups only | About 10 search queries ran, then the shared per-IP daily budget was exhausted (HTTP 429 with `retry-after` of about 8 h, "free daily budget shared by everyone on your network's IP address"). After that only `/works/doi:...` and `/works/W...` single-entity lookups were used (they report 0 credits): open-access locations for about 190 DOIs, and the reference lists of 13 seed papers (Onica survey, Uzunov, Esposito, Tariq, Cui TDSC, 2PPS, Dahlmanns, LCMsec, Pub/Sub-meets-MLS, Barazzutti TDSC, AnonPubSub, SCBR, Park 2025) for backward citation chasing. The chase of the later seeds was cut short for time (725 of 772 references resolved). |
| Crossref | `query.bibliographic`, rows 60, `from-pub-date:2011` | 185 queries (privacy/confidentiality/ABE/IBE/searchable encryption/subscription privacy/anonymity/PIR/OMR/mixnet/onion/DC-net/DP/trust/censorship/DoS/RLN/MPC/ZK/blockchain/DDS/ROS/access control/Byzantine); about 6,200 distinct DOIs seen, screened by title regex, then read by hand. Also used for DOI/title resolution of seed titles. |
| arXiv API | title and abstract searches | 21 + 43 query expressions (pub/sub with privacy, anonymity, SGX, ABE; GossipSub attacks; metadata-private messaging; OMR; DC-nets; mixnets; RLN; Dandelion; censorship; libp2p; Waku ...), 100 results per page. Two long 429 episodes; title lookups of metadata-only records were stopped after about 60 tries with no hit. |
| Semantic Scholar | batch endpoint for metadata and `openAccessPdf`; search | Search and match endpoints were throttled almost permanently (429 / time-outs); 7 search queries and about 12 title matches completed. The POST `/paper/batch` endpoint worked 5 times and supplied abstracts, venues and OA links for about 440 identifiers. |
| HAL | `api.archives-ouvertes.fr` | 28 queries on titles/abstracts; produced 14 records and several PDF links. Queries on "onion" return vegetable papers, avoid that word. |
| IACR ePrint | `eprint.iacr.org/search?q=` (HTML) | 40 queries; six records added, five existing records got an ePrint PDF. One short 429. |
| OpenAIRE | `api.openaire.eu/search/publications` | One lookup per record without a PDF (DOI or title); gave 26 extra candidate URLs, 8 of which delivered a PDF. |
| Publisher / repository pages | direct PDF links from the sources above | `usir.salford.ac.uk` and `downloads.hindawi.com` answered 403 (not retried); `orbilu.uni.lu` has an unusable TLS chain; ieeexplore/ACM/Springer PDF links from OpenAlex mostly return HTML and were treated as unavailable. |
| WebSearch | about nine confirmation searches early on | The session-wide search cap (200 calls, shared with other agents) was then exhausted, so discovery of author home pages by web search was not possible. |

DBLP, CORE and Unpaywall were not used (blocked / needs an e-mail).

## Counts

- Records written: 124; downloaded 57; metadata_only 67; not_found 0.
- Every downloaded file starts with `%PDF-` and its sha256 matches the catalog. The first pages of all downloads were text-matched against the title; all pass except the Klingler thesis (French title, checked by hand: correct document).
- Years: the catalog `year` is the earliest public version; where an arXiv version is earlier or later this is stated in the note.

## Records that overlap other slices

None at the last run (checked on DOI, arXiv id and normalised title against every other `catalog/*.jsonl`). Mid-run G-surveys-citations listed several of the same papers as metadata_only (for example `2015-onica-efficient`, `2023-pei-efficient`, `2022-klingler-confidentialite`); by the final run those entries were no longer in G, so the records stay here with their PDFs. If G re-adds them, keep the copy that has the PDF. The catalog set changes quickly, so the lead should re-run the duplicate check before merging.

## Incident worth knowing

Mid-run, about 80 of my own downloads were deleted because they duplicated papers that other slices catalogue. Ten of those files had the same slug (and so the same path) as files that D, G, PB3 or PB4 list, so for a while those catalogs pointed at missing files. I re-downloaded all ten from the URLs recorded in the other slices' catalogs. Nine match the catalogued sha256. For `2015-borisov-dp5.pdf` (PB3) the file at the source URL has changed since it was first fetched, so the restored file is the same paper but its sha256 no longer matches PB3's record; PB3's sha256 needs updating (a full check also showed `2023-balbas-sender-keys` in PB6 with a differing sha256, which is not my file). The finalisation script now refuses to delete any path that appears in another slice's catalog. The lead should still run a check that every `downloaded` record in every catalog has a file on disk.

## Papers wanted but not obtained (metadata_only, core)

Core records without an open copy (publisher link in `landing_url`):

- Cryptographic protocol for secure dissemination of notification messages (2011) 10.1109/iccp.2011.6047905
- Conflict Detection and Lifecycle Management for Access Control in Publish/Subscribe Systems (2011) 10.1109/hase.2011.50
- Security Policy and Information Sharing in Distributed Event-Based Systems (2011) 10.1007/978-3-642-19724-6_7
- EventGuard: A System Architecture for Securing Publish-Subscribe Networks (2011) 10.1145/2063509.2063510
- Thrifty privacy: efficient support for privacy-preserving publish/subscribe (2012) 10.1145/2335484.2335509
- Design and implementation of a confidentiality and access control solution for publish/subscribe systems (2012) 10.1016/j.comnet.2012.02.013
- Performance/Security Tradeoffs for Content-Based Routing Supported by Bloom Filters (2013) 10.1007/978-3-319-03578-9_11
- An efficient privacy preserving Pub-Sub system for ubiquitous computing (2013) 10.1504/ijahuc.2013.051374
- The overlay scan attack (2014) 10.1145/2611286.2611295
- Policy enforcement within emerging distributed, event-based systems (2014) 10.1145/2611286.2611310
- Towards a cryptographic treatment of publish/subscribe systems (2014) 10.3233/jcs-130486
- The Pairing-Based Cryptography Mechanism to Provide Confidentiality and Authentication for Broker-Less Content (2015) https://www.semanticscholar.org/paper/5abd4d5ac92a9cf1a89d5f740ac90e29f2b50106
- Applying Attribute-Based Encryption on Publish Subscribe Messaging Patterns for the Internet of Things (2015) 10.1109/dsdis.2015.52
- Privacy-preserving publish/subscribe service in untrusted third-party platform (2016) 10.1109/icc.2016.7511192
- Efficient key management for publish/subscribe system in cloud scenarios (2016) 10.1504/ijhpcn.2016.080422
- Secure Data-Centric Access Control for Smart Grid Services Based on Publish/Subscribe Systems (2016) 10.1145/3007190
- Secure Content Delivery in Publish-Subscribe Networks (2017) https://www.semanticscholar.org/paper/fa22bb0892c81f22665e79c7623f61c012225dc5
- PICADOR: End-to-end encrypted Publish-Subscribe information distribution with proxy re-encryption (2017) 10.1016/j.future.2016.10.013
- Mitigating DoS attacks in publish-subscribe IoT networks (2017) 10.1109/ecai.2017.8166463
- Adopting Attribute-Based Access Control to Data Distribution Service (2017) 10.1109/icssa.2017.23
- Privacy-preserving attribute-keyword based data publish-subscribe service on cloud platforms (2017) 10.1016/j.ins.2016.09.020
- Secure publish and subscribe systems with efficient revocation (2018) 10.1145/3167132.3167176
- Attacking OMG Data Distribution Service (DDS) Based Real-Time Mission Critical Distributed Systems (2018) 10.1109/malware.2018.8659368
- Securing Publish/Subscribe (2018) https://hdl.handle.net/11572/368098
- Scalable Identity and Key Management for Publish-Subscribe Protocols in the Internet-of-Things (2019) 10.1145/3365871.3365883
- Privacy-Preserving Content-Based Publish/Subscribe Service Based on Order Preserving Encryption (2019) 10.1007/978-3-030-38651-1_31
- From Confidential kNN Queries to Confidential Content-based Publish/Subscribe (2019) 10.5220/0007950506770682
- A Revocable Publish-Subscribe Scheme Using CP-ABE with Efficient Attribute and User Revocation Capability for  (2019) 10.1109/icece48499.2019.9058563
- Cloud-assisted secure and conjunctive publish/subscribe service in smart grids (2020) 10.1049/iet-ifs.2019.0086
- A topic‐centric access control model for the publish/subscribe paradigm (2020) 10.1002/cpe.5614
- Practical Anonymous Subscription with Revocation Based on Broadcast Encryption (2020) 10.1109/icde48307.2020.00028
- Transparent End-to-End Security for Publish/Subscribe Communication in Cyber-Physical Systems (2021) 10.1145/3445969.3450423
- MagikCube: Securing Cross-Domain Publish/Subscribe Systems with Enclave (2021) 10.1109/trustcom53373.2021.00037
- Flexible and Efficient Security Framework for Many-to-Many Communication in a Publish/Subscribe Architecture (2022) 10.3390/s22197391
- Privacy-preserving data dissemination scheme based on Searchable Encryption, publish-subscribe model, and edge (2023) 10.1016/j.comcom.2023.03.006
- Verifiable Cloud-Based Data Publish-Subscribe Service With Hidden Access Policy (2023) 10.1109/tcc.2023.3326339
- Secure Cloud-Assisted Data Pub/Sub Service With Fine-Grained Bilateral Access Control (2023) 10.1109/tifs.2023.3303720
- Publish Subscribe System Security Requirement: A Case Study for V2V Communication (2024) 10.1109/ojcs.2024.3442921
- DDS Security+: Enhancing the Data Distribution Service With TPM-based Remote Attestation (2024) 10.1145/3664476.3670442
- A Formal Analysis of Data Distribution Service Security (2024) 10.1145/3634737.3656288
- LCM-RA: Secure and Attestation-Enabled Publish/Subscribe for Dynamic Groups (2025) 10.1109/vtc2025-fall65116.2025.11310236
- Data Distribution and Redistribution - A formal and practical Analysis of the DDS Security Standard (2025) 10.1145/3672608.3707869
- BI-MQTT: Broker-Independent Integrity for Publish–Subscribe Messaging with Ring Signatures (2025) 10.1109/cascon66301.2025.00104
- Privacy-preserving cloud-agent pub-sub system with decentralised authorisation and bilateral fine-grained acce (2026) 10.1504/ijics.2026.154875
- Proof-Carrying Payloads: End-to-End Authorization for Pub/Sub Messaging (2026) 10.1016/j.jlamp.2026.101173

Several probably have free author or institutional copies that I could not reach with the tools available (no web search): for example Thrifty privacy, EventGuard, the Ion Computer Networks paper, and the DDS-security papers (KIT and Stuttgart repositories were listed by OpenAIRE but returned no PDF). Bischof's 'Non-functional requirements in publish/subscribe systems' thesis (Stuttgart OPUS, DOI `10.18419/opus-3088`) is not in Crossref and was left out of the catalog.

## Gaps and seeds for other slices

- Not found: a pub/sub paper whose main mechanism is secure multiparty computation (the only zero-knowledge one is DPS-IIoT); differential-privacy pub/sub beyond PCP (held elsewhere), Pufferfish event times and the gossip-privacy results; DoS or Sybil analyses of Kademlia-based pub/sub beyond GossipSub (slice C).
- Confidentiality-preserving engines by the Neuchatel/Onica group are only partly covered: StreamHub (DEBS 2013, `10.1145/2488222.2488260`) and Elastic Scaling of a High-Throughput Content-Based Pub/Sub Engine (ICDCS 2014, `10.1109/icdcs.2014.64`) appear in the Onica survey's references but in no catalog.
- The DDS (brokerless) security thread (Lauser 2025, Wang ASIACCS 2024, Wagner 2024, Michaud 2018, Murugesan 2017) fits slice F; there are more DDS/ROS 2 security papers (SROS2, RTI Connext security evaluations) that I did not chase.
- Byzantine peer sampling (Basalt, AUPE, Brahms) belongs with slice A; Brahms itself is 2008 and out of range.
- The 2024-2026 mixnet and anonymous-broadcast papers I found were all already in PB2; a full pass over the USENIX Security / PoPETs / NDSS 2024-2026 programmes for pub/sub-like or channel APIs is still open.
- Backward chase of the 2018-2025 seeds (Cui, 2PPS, Dahlmanns, LCMsec, MLS, Park) stopped at 725 of 772 references; the remaining ones are unreviewed.
