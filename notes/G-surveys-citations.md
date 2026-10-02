# G-surveys-citations: cross-cutting sweep (surveys, theses, citation chase, odd vocabulary)

Result: 321 records in `catalog/G-surveys-citations.jsonl` (70 downloaded, 251 metadata_only, 0 not_found; 267 core, 54 adjacent).
About 180 further candidates were dropped at write time because another slice (mostly A, E, D, F) already had the same DOI, arXiv id, normalised title or PDF hash. Seven records that I wrote before other slices caught up were removed at the end for the same reason.

## What blocked or limited me

- **OpenAlex was unusable.** Within minutes of starting, the free per-IP daily budget (shared with every other agent on this machine) was used up: HTTP 429 with `retryAfter` about 29000 s. I did not use a key or any workaround. The `filter=cites:` chase and the OpenAlex terminology sweeps were therefore done with substitutes (below). Seeds were resolved by DOI through Crossref instead.
- arXiv API: frequent 429/503 under load; the sweep needed a slow second pass (`ax2`). Three query phrasings (selective dissemination, federated pub/sub, multi-broker) never returned a page and were not retried.
- Semantic Scholar: works only after 429 back-offs (30 s); the `paper/search/match` calls for author repair took about an hour.
- DBLP, ResearchGate, publisher "generatepdf" links: not fetched (one DBLP record page was hit once by mistake via an OpenAIRE URL and answered 429; I then blacklisted the host). Publisher hosts (IEEE, Springer, ACM, Elsevier) returned 403 or HTML for paywalled items: recorded as metadata_only.
- No Unpaywall, no Sci-Hub, no email in any request. User-Agent was `privateEventsResearch/1.0` (pe_fetch default).

## Substitute sources used (all open, no key, no email)

| Need | Source |
|---|---|
| forward citations | OpenCitations COCI/index v2 (`/index/v2/citations/doi:...`) resolved to titles with Crossref `filter=doi:`; Semantic Scholar graph `/paper/{id}/citations` (paged, 500 per page) |
| terminology sweeps | Crossref `query.bibliographic` (102 queries x 100), arXiv API (51 phrase queries), OpenAIRE Graph API `researchProducts` (40 general queries x 5 pages; 22 queries x 4 instance types for theses, books, chapters), HAL API (22 queries x THESE/HDR/OUV/COUV) |
| metadata and OA PDF URL | Semantic Scholar `/paper/batch` (`openAccessPdf`), OpenAIRE instances, HAL `/document`, repository `citation_pdf_url` meta tags |

## Citation chase

Seeds and the number of 2011+ citing papers seen (OpenCitations / Semantic Scholar):
PolderCast 44/95, Vitis 102/250, SpiderCast 93/136, Meghdoot 56/95, Hermes 203/242, GossipSub (arXiv 2007.02754) -/84, Plumtree 59/110, HyParView 65/113, Scribe 911/576, Cyclon 335/358, Kademlia 1380/2168.
Kademlia, Scribe and Cyclon were filtered by title/abstract keywords (pub/sub, multicast, dissemination, gossip, overlay, topic, broker, rendezvous, messaging) and then judged by hand against the inclusion test; most Kademlia citations are file sharing, blockchain broadcast or search, and were dropped.
Pre-2011 seeds themselves (Scribe 2002, Meghdoot 2004, Hermes 2002, SpiderCast 2007, Plumtree 2007, HyParView 2007, Cyclon 2005, Kademlia 2002) are excluded by the year rule.
Surveys chased the same way (Semantic Scholar only): Onica et al. confidentiality survey, Esposito security survey, security-solutions survey, reliability survey and tutorial, WSAN pub/sub survey, QoS in wide-scale pub/sub, P2P pub/sub encyclopedia entry, P2P overlay survey for virtual environments, DOSN taxonomy, others. They yielded few new items (most hits were IoT security or DOSN privacy papers outside scope).

## Surveys, theses, chapters found

About 22 title-level surveys/reviews/tutorials and 25 theses/dissertations/book chapters, tagged `survey` / `thesis` in the catalog. Theses came from OpenAIRE (Doctoral thesis / Master thesis filters) and HAL (OpenAIRE aggregates them), for example: Zhang (gossip pub/sub in P2P, 2015), Setty (pub/sub for social interaction, 2015), Daubert (AnonPubSub, 2016), Onica (privacy-preserving pub/sub, 2016), Ion (security of pub/sub, 2013), Richerzhagen (mechanism transitions, 2017), Lehn (InterestCast, 2016), Amozarrain (fully mobile pub/sub, 2021), de Araujo (causal broadcast pub/sub, 2019), Pace (gossip in the wild, 2011), Boutet (decentralized news personalisation, 2013), Khazaei, Geng, Shen, Zaarour, Iglesias, Khoury, Kadimbadimba, Ginzler, Layazali, Costa (epidemic broadcast under Byzantine faults).
Gap: I did not find a stand-alone "SoK" on decentralized pub/sub. The closest are Onica et al. (confidentiality), Esposito et al. (security, reliability), the Edge Intelligence systematic review (2026) and a 2026 survey of broadcast mechanisms in P2P overlays.

## Terminology sweeps (phrases that produced new, in-scope records)

event notification service; brokerless / broker-less (ZeroMQ-style, DDS, MQTT-without-broker, D-MQTT, MQTT2EdgePeer); serverless publish/subscribe; decentralized message bus (Iris, DZMQ, microservice bus); rendezvous routing (Vitis/Vinifera, geo-context rendezvous, BubbleStorm); interest-based dissemination (opportunistic networks, InterestCast, Spotify); P2P social-network feeds and news personalisation (SELECT, Boutet thesis, P2P/DOSN surveys, Secure Scuttlebutt); group communication overlays (P2PPS and causal-order work of Nakayama/Nakamura/Saito; multi-layered group communication); application-level multicast (kept only Scribe-style DHT multicast, DRScribe, Scribe-based surveys; generic streaming-tree ALM papers were judged out of scope and dropped); Waku / Waku-RLN-Relay; formal GossipSub analyses; PSIRP/ICN publish/subscribe internetworking.
Noise-heavy queries (Crossref "subscription", "messaging", "epidemic", "gossip") returned economics, medicine and sociology; these were filtered out by regex plus manual review.

## Selection rules actually applied

- Core: title shows pub/sub, event notification, topic/content-based routing, brokerless, GossipSub/Waku, rendezvous or event dissemination, and the paper is decentralized, P2P, gossip/DHT/overlay, broker-mesh/multi-broker, ad hoc/opportunistic, ICN, blockchain, brokerless, or privacy/security for such systems.
- Adjacent: gossip/epidemic broadcast, peer sampling, group communication, DHT multicast, P2P social networks and surveys of those, only when cited by or clearly used in pub/sub work.
- Dropped: single-broker cloud services, matching algorithms for one server, OPC UA, plain MQTT/Kafka studies, searchable-encryption cloud pub/sub, subscription-economy hits, patents.

## Wanted but not obtained (metadata_only: no legal open copy found)

251 records are metadata_only, nearly all IEEE/Springer/ACM/Elsevier papers whose only copy is behind a paywall (examples in this slice: COPSS, Pyracanthus, Marshmallow, v-CAPS, On-Line Optimization of Pub/Sub Overlays, Quality of Service in Wide Scale Pub/Sub). Authors' home pages were not crawled; a later pass using arXiv title search or author pages could convert some of them.
Forward-citation lists are limited to what OpenCitations and Semantic Scholar index, because OpenAlex was unavailable (arXiv-only citers of PolderCast/Vitis may be missing).

## Hand-offs to other slices (topics where this sweep found papers other slices should double-check)

- A (gossip/topic): the Nakayama/Nakamura/Saito P2PPS series (topic-based synchronisation, causal ordering, information-flow control) has many more members than are in the catalog; the minimum topic-connected overlay line (Hosoda, Chen, Rahimian) is mostly in A.
- B (DHT): KATT (hierarchical Kademlia telemetry transport, 2025), DHT-based pub/sub under churn, Pyracanthus and Marshmallow (kept here as metadata_only).
- D (blockchain): pub/sub with blockchain (BPS, BREPubSub, Galaxy, DPPS, Secure Pub-Sub with fair payment); other slices may already hold more.
- E (privacy): Daubert's AnonPubSub work, Di Crescenzo's private pub/sub protocols, v-CAPS, Nikander's "pure pub/sub" cryptographic protocols.
- F (edge/IoT/ICN): PSIRP-era papers (Xylomenos, Giannaki, Lagutin, Carrea), COPSS and COPSS-lite, NDN pub/sub, DDS discovery, brokerless microservice IoT platforms (IoHT-MBA, SIP-MBA) which I judged too weak to include.
- Suggested seeds to chase: Esposito/Platania/Beraldi "Resilient and Timely Event Dissemination" family, the MAKI "mechanism transitions" family (Richerzhagen, Kuhn), XRPL/GossipSub measurement papers (2023-2025).

## Intermediate artifacts

Working scripts and raw candidate dumps live in the session scratchpad, not in the repository.
