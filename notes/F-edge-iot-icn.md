# Slice F-edge-iot-icn: edge, IoT, information-centric and federated pub/sub (2011-2026)

Catalog: `catalog/F-edge-iot-icn.jsonl` (380 records, 105 downloaded, 275 metadata_only, 0 not_found).
Relevance: 356 core, 24 adjacent (CRDT and local-first, NDN dataset sync, DDS discovery with Bloom filters, XMPP, Zenoh/ROS 2 performance).
All 105 PDFs were checked: `%PDF-` header, sha256 matches the catalog, and at least 60% of the title words appear on the first three pages.

## Source situation on 2026-10-01 (important for anyone repeating this)

- **OpenAlex is unusable.** The first request returned 429 with "Insufficient budget ... free daily budget shared by everyone on your network's IP address ... resets at midnight UTC" (retry-after about 29,000 s). Another agent's earlier traffic had used the shared budget. No OpenAlex data in this slice.
- **arXiv API** answered 429 or 503 for most of the session. A background script with 20-90 s back-off finished 58 queries (198 unique entries) after about 40 minutes.
- **Semantic Scholar**: the `paper/search` endpoint answered 429 almost always (2 of 41 queries succeeded). The `paper/batch` POST endpoint worked (100 DOIs per call) and gave `openAccessPdf`, `externalIds` and `tldr`. It is the main source of legal open-PDF links and of the one-line notes.
- **Crossref** (no email parameter, `query.bibliographic`, 30-60 rows) worked for 239 query runs and returned 4,318 unique works. It is the discovery backbone for this slice.
- **HAL** API worked: DOI lookups for every candidate plus 52 keyword runs (`publish subscribe`, `MQTT`, `DDS discovery`, `zenoh`, `CRDT`, ...). HAL PDFs (`/document`) are the cleanest legal copies.
- **Europe PMC** (`search?query=DOI:` then `europepmc.org/articles/PMCxxx?pdf=render`) gave 8 more open copies for Sensors and other PMC-indexed journals. The older `ptpmcrender.fcgi` URL returned 520.
- **fatcat.wiki** reset the connection. Not used.
- **Bot walls and logins, not bypassed:** MDPI PDF URLs (JavaScript challenge page, 2 KB HTML), dl.acm.org (403), sciencedirect.com and doi.org/10.1016 landing pages, IEEE Xplore (login/proxy), NCBI PMC PDF (proof-of-work page), research.rug.nl and hdl.handle.net (403). Zenodo records 3448590, 3431447 and 3434134 are tombstones (410). Those papers stay metadata_only.
- The shared scratchpad was overwritten once by another agent's `harvest.py`; this slice worked in its own subfolder afterwards.

## Queries run

Crossref (239 runs, title/abstract-level matching, then manual title triage of about 2,300 hits): broker-less / decentralized / federated pub/sub, MQTT broker bridging, clustering, federation, MQTT-ST, DDS discovery (Bloom filter, DHT, discovery server, WAN routing), Zenoh, ROS 2 discovery, fog and edge pub/sub, broker placement, multi-broker overlays, NDN/CCN/ICN pub/sub (COPSS, G-COPSS, PSIRP/PURSUIT, PSync, ChronoSync, IoT-NDN, vehicular NDN), SDN and P4 pub/sub (PLEROMA, OpenFlow, TCAM, programmable data planes), WSN, VANET, MANET, DTN and opportunistic pub/sub, serverless and event mesh, WebRTC and browser P2P, CRDT and local-first, XMPP/AMQP/CoAP, survey and comparison papers, geo-distributed overlays, 5G/MEC, satellites, UAV, LoRa, Bluetooth mesh, smart grid, OPC UA PubSub.

arXiv (58 queries, e.g. `all:"publish/subscribe" AND all:"named data"`, `all:zenoh`, `all:"MQTT" AND all:federation`, `all:"CRDT" AND all:"pub/sub"`, `all:"event mesh"`, `all:libp2p`, `all:PSync`). Semantic Scholar batch lookup of every candidate DOI (555 DOIs, 500+ resolved). HAL as above.

## Inclusion decisions

Kept: pub/sub or topic/content-based dissemination that is distributed, P2P, federated, multi-broker, ICN-based, SDN/P4-based, broker-less, DTN/MANET/VANET/WSN-based, edge/fog-hosted, serverless, plus surveys and comparisons of pub/sub middleware and DDS/MQTT/Zenoh decentralization mechanisms, plus theses found on HAL.

Not kept (title-level judgement; may deserve a second look by the lead):
- OPC UA PubSub, TSN, plain MQTT-over-TLS, MQTT security, intrusion detection and fuzzing papers (single-broker).
- CoAP Observe congestion control, MQTT/CoAP/AMQP protocol performance comparisons on one broker.
- ICN/NDN papers on caching, forwarding, security and routing that are not about subscriptions.
- Pure CRDT papers without a subscription or sync-over-pub/sub angle (only the Shapiro 2011 paper, delta CRDTs, the CRDT survey, the local-first essay, edge CRDT sync work and similar were kept as adjacent).
- General content-based matching algorithm papers (a single-node matching engine), privacy-preserving encrypted matching, access-control schemes for one broker: these belong to other slices.
- Kafka/RabbitMQ/cloud Pub/Sub enterprise usage papers.

Duplicates: a paper whose DOI, arXiv id or normalised title is already in another slice is skipped when that slice already has the PDF, or when this slice has no PDF. 253 candidates were skipped on that rule (checked at the end of the run against all catalog files then present). Where this slice holds a PDF and another slice has only metadata, the record is kept here.

## Wanted but not obtained (metadata_only in this catalog, notable)

Gaming over COPSS / G-COPSS (ICNP 2011, ICDCS 2012), COPSS-lite (journal listing; the arXiv copy is in slice G), PLEROMA (Middleware 2014) and its ToN follow-up "High Performance Publish/Subscribe Middleware in Software-Defined Networks" (Bhowmik et al. 2017), ChronoSync (ICNP 2013), "Scalable name-based data synchronization for NDN" (INFOCOM 2017), "Supporting pub/sub over NDN sync" (ICN 2021), Zenoh dataflow and programmable-dataplane papers (2021-2022), BORDER (JIoT 2022), EdgePub (FMEC 2022), the Koziolek MQTT broker comparison (2020), Kleppmann's local-first essay (Onward! 2019; the repository link returned a landing page), Cyclon over WebRTC (P2P 2015), and most IEEE and ACM conference papers on SDN/P4 pub/sub, VANET and WSN pub/sub. Each has a DOI and landing URL in the catalog. COPSS (ANCS 2011) itself is already recorded as metadata_only in slice G, so it is not repeated here.

## Seeds for other slices

- GossipSub / Floodsub: arXiv 2507.19013 (Floodsub correctness), 2212.05197 and 2311.08859 (GossipSub verification), 2007.02754 (Filecoin/ETH2 GossipSub), 2505.17337 and 2504.10365 (libp2p GossipSub large messages), 2207.00117 (Waku RLN relay), 2508.04833 (OptimumP2P). Slice C probably has some.
- Decentralized messaging and metadata: 2401.09102 (SendingNetwork), Matrix analyses (10.1109/sp54263.2024.00075, 10.1109/iwqos70441.2026.11661051), 10.1145/3460120.3484542 (decentralized group messaging key agreement), 10.1145/3428662.3428794 (Secure Scuttlebutt gossip with append-only logs), 2402.16201 (Honeybee peer sampling).
- Privacy and confidentiality in pub/sub: arXiv 1705.09404 (survey), 10.1016/j.cose.2016.04.008 (security survey for distributed pub/sub), 10.1145/2295136.2295164 (P3S-style privacy preserving content-based), 10.1007/978-3-642-35170-9_24 (P3S middleware).
- Blockchain pub/sub: 2101.12331 (pub/sub for blockchain interoperability), 1807.03110 (Trinity), HyperPubSub (10.1145/3155016.3155018, on HAL as hal-02176333).
- Browser P2P and sync: Cyclon over WebRTC (10.1109/p2p.2015.7328517) was kept; Spray, CRATE and Yjs/Automerge-style system papers were not found by these queries and could be chased by a dedicated local-first query.
- Not chased: PURSUIT/PSIRP deliverables and SIENA/Rebeca/Hermes-era papers are pre-2011.

## Gaps

- Only 28 percent of the records have an open PDF because most papers in this area are IEEE, ACM or Elsevier closed copies and the usual open-access discovery services (OpenAlex, Unpaywall) were unavailable. A rerun after the OpenAlex budget resets (midnight UTC) with `best_oa_location` on the metadata_only DOIs would likely add a further 50-100 PDFs.
- Abstract-based notes are missing for 132 records; their `note` field says so.
- Semantic Scholar search and arXiv were throttled, so recall for 2024-2026 arXiv preprints may be below that of the 2011-2023 Crossref coverage.
