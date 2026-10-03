# C-gossipsub-libp2p: collection notes

Slice: libp2p and blockchain-network era of pub/sub, 2015-2026. Run on 2026-10-01.
Catalog: `catalog/C-gossipsub-libp2p.jsonl` (64 records: 44 downloaded, 20 metadata_only, 0 not_found).
The 44 downloaded PDFs are in `pdfs/`; every downloaded file starts with `%PDF-` and matches its recorded sha256.

## What the catalog contains
- GossipSub: the 2019 PL technical report, the 2020 paper, the v1.1 evaluation report, the Least Authority v1.1 audit, formal models (ACL2s, Floodsub correctness), parameter studies (Lean Gossip), XRPL/GossipSub studies (5 papers), large-message work (Staggering, PREAMBLE), a Lancaster MRes thesis on GossipSub for DAS.
- libp2p specs (metadata_only, landing_url = GitHub spec; no PDFs exist): pubsub interface, gossipsub v1.0, v1.1, v1.2, v1.3, partial-messages, Episub, RED. Plus the Ethereum consensus-layer p2p spec and the IPNS PubSub Router spec.
- Waku and RLN-relay: 5 papers (Waku family, RLN-relay, spam-protected gossip, latency, Waku Network for dApps).
- Network-coded and structured broadcast: OptimumP2P (+demo), Optimum Peer-Turbo, Kadcast, Kadcast-NG, Bromberg et al. (network-coded rumor spreading).
- Pub/sub systems on IPFS/libp2p/blockchain: SmartPubSub, Pulsarcast, Topiary, Streamr (2 papers), the cellular-automata-on-IPFS-PubSub paper.
- Attacks, privacy, measurement: Deanonymizing Ethereum Validators, Tor-based validator privacy, Eth2 P2P discovery/measurement, Honeybee, Kiffer et al. (Ethereum gossip), Eth2.0-NA, CliqueSensus.
- Adjacent building blocks: Perigee, Fabric gossip, PANDAS and DAS networking (2 papers + Kademlia DAS), Duet, Frey et al. differentiated gossip.

## Queries run
- arXiv API (phrase searches): gossipsub, GossipSub, libp2p, Plumtree, HyParView, "epidemic broadcast tree", peer scoring, Waku, RLN relay, IPFS pubsub, gossip + Ethereum, block propagation, RLNC, eclipse + gossip, data availability sampling + gossip, Dandelion, Kadcast, Perigee, erasure + gossip, network coding + blockchain, smart contract pub/sub, pubsub + p2p, lean gossip. Counts were small (0-15 relevant per query); results are in the catalog.
- Crossref bibliographic search (GossipSub/libp2p; gossip pub/sub blockchain; Ethereum block propagation network coding) and Crossref DOI lookups for authors and venues.
- HAL API: libp2p, gossipsub, IPFS pubsub, XRP dissemination and others. Source of 5 open PDFs (XRPL mesh causal, Squelch, Tumas, Frey, Bromberg).
- Semantic Scholar: DOI lookups (open-access links), and forward citations of arXiv:2007.02754 (GossipSub, 84 citing papers read), 2212.05197, 2409.04366, 2504.10365, 2207.00117, 2508.04833, 2312.06800.
- Reference-list mining of 12 downloaded PDFs (pdftotext) for further pub/sub and gossip citations.
- Web search was used for about 40 discovery queries before the session budget (200) ran out.

## Hosts that blocked or limited me
- OpenAlex: 429 on nearly every call (shared IP, many agents). No OpenAlex result was usable after the first query; a few early OpenAlex hits are recorded as `found_via: openalex`.
- arXiv API: repeated 429s; late metadata calls returned non-XML. PDFs via arxiv.org/pdf worked.
- Semantic Scholar search endpoint: 429 throughout; the DOI and citations endpoints worked.
- eprint.iacr.org: occasional 429 (Generals' Scuttlebutt PDF not fetched; it is in `iog-library` anyway).
- dl.acm.org: HTTP 403 bot wall. doi.org to ACM and IEEE: 403 / 202. Not bypassed.
- orbilu.uni.lu: TLS certificate chain fails verification. Not bypassed (no insecure mode).
- WebSearch budget exhausted partway; HAL and Crossref carried the rest.

## Wanted but not obtained (metadata_only records with a known route)
- Three Uni Luxembourg XRPL/GossipSub papers (Pub/Sub Dissemination on the XRP Ledger; 9-dimensional Analysis; Causal AI for XRPL/GossipSub). Open PDFs exist at orbilu.uni.lu (URLs in the `note` fields) but the host's TLS chain is broken. Retry later or look for HAL copies.
- CliqueSensus (Middleware 2025, ACM OA), the Broadcast Mechanisms survey (IEEE Access OA): publisher bot walls.
- Kiffer et al., "Under the Hood of the Ethereum Gossip Protocol" (FC 2021): Springer, no open copy found.
- Eth2.0-NA (INFOCOM 2026), Lee et al. APNOMS 2025, duplicate-reception ICBC 2026, Tapolcai ICDCS 2025: no open copy located.

## Left out on purpose (pre-2011 or out of scope)
- Plumtree/Epidemic Broadcast Trees (SRDS 2007) and HyParView (DSN 2007): pre-2011, so excluded by the year rule. Open PDFs exist at asc.di.fct.unl.pt/~jleitao/pdf/ if the lead wants them as background.
- Generals' Scuttlebutt (CCS 2022), Cardano data-diffusion design, SCRamble, CougaR: already in `catalog/iog-library.jsonl`. The Cardano network design document states that pub/sub and multicast are explicitly out of its design.
- Execution-layer/other: Eclipse Attacks on Ethereum's P2P (discovery layer, WWW 2026), Routing Attacks in Ethereum PoS, Tikuna, Security Review of Ethereum Beacon Clients, DAS simulation study (2407.18085), Goldfish, BSB, StarveSpam, Mercury, Merkle-CRDTs, Dandelion++, "The latest gossip on BFT consensus", Ferretti 2011 "Pub/sub via gossip" (generic gossip pub/sub; another slice should take it).
- Waku spec pages (lip.logos.co / rfc.vac.dev) returned 404 or redirect loops, so no Waku spec records. The Gossipsub v2.0 (PR #653) and topic-observation (PR #617) proposals are pull requests, not merged specs, so not recorded.

## Seeds for other slices
- Ferretti, "Publish-Subscribe Systems via Gossip" (arXiv 1112.0416, 2011).
- OpenPubSub (Zaarour, Bhattacharya, Curry, IEEE IoT J. 2022) and Vitis, Spidercast (cited by Topiary).
- Bakhshi/Gavidia/Fokkink/van Steen, "A modeling framework for gossip-based information spread" (QEST 2011).
- Swarm PSS, Nostr, Farcaster Hubs (GossipSub-based), Secure Scuttlebutt: decentralized messaging on pub/sub.
- Trinity (arXiv 1807.03110, blockchain pub/sub broker) surfaced in a search.
- Cited-by lookups on Topiary and Perigee would be worth a pass once the APIs cool down.

## Data caveats
- `cited_by` is null throughout (no reliable citation source was reachable).
- Spec records use the earliest known year (gossipsub v1.0 and pubsub interface 2018, Episub 2018); revision dates are in the notes.
- The 2019 PL technical report lists two authors on its title page (Vyzovitis, Psaras); other sources list four.
- Several author lists came from arXiv API, Crossref or the PDF title page; none were taken from memory without a check.
