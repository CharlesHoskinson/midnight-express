# Slice B-dht-content: notes

Catalog: `catalog/B-dht-content.jsonl`, 78 records (50 core, 28 adjacent): 19 downloaded, 59 metadata_only, 0 not_found.

## Why the catalog is small

I assembled about 306 in-scope candidates (OpenAlex, Crossref, arXiv, own knowledge). 228 of them were already in
other slices' catalogs (A-gossip-topic held about 106 of the first 301, and D, F, G and C added more later), so
they were dropped under the de-duplication rule. The 78 left are the part of the scope that no other slice
had taken at the time of the final check (2026-10-01). If A-gossip-topic or others drop records, re-run a title/DOI
check: some of the 228 may then be orphaned. Overlap was heaviest for DHT/topic-based overlay design,
Scribe-style trees, Banno/Teranishi, Nakamura/Nakayama P2P pub/sub, self-stabilizing pub/sub, spatial (VSO) and MANET (Tchembe, SocialMANET).

## Queries run

- OpenAlex `search=` with `from_publication_date:2011-01-01`, 2 pages x 100: 10 queries (DHT-based pub/sub, distributed hash table
  pub/sub, content-based P2P, structured overlay, Scribe, Chord, Kademlia, Pastry, subscription covering, subscription merging;
  1,416 unique works). Then the shared-IP free budget hit zero (429 "Insufficient budget", resets midnight UTC), so the other 20
  planned queries (range query, multi-attribute, rendezvous, churn, geo, semantic, MANET, VANET, DTN, stream processing, surveys,
  brokerless, ...) were run on Crossref instead. Single-work lookups `works/doi:...` kept working and were used for OA locations of all picks.
- Crossref `query.bibliographic` from 2011, 100 rows each: about 100 queries covering all the topics in the scope line plus
  author/title probes (Spotify, PolderCast, Setty, Rahimian, Chockler, Jacobsen group, Dynamoth, Yoneki, Carzaniga, Hermes,
  RSS/microblogging, skip graph, Hilbert curve, interest management, hypercube, RELOAD/data-centric). Results were filtered by title
  keywords and read by hand; Crossref ranking is noisy (spacecraft rendezvous, "wide-area" power systems, CEP textbooks).
  The last three batches added almost nothing in scope, so I consider the scope saturated for these sources.
- arXiv API: 7 phrase queries (publish/subscribe, pub/sub, DHT, content-based, topic-based, pubsub P2P; 2 pages of the main phrase),
  about 400 records read; then 429 for the rest of the session. arXiv has few papers in this scope (14 picked or paired).
- Semantic Scholar: `POST /paper/batch` for DOIs (`openAccessPdf`), after 429 back-offs. Single-paper GET was 429.
- Wayback CDX for `msrg.org/publications/pdf_files/` (Jacobsen group); archived copies of the authors' own PDFs fetched via `web.archive.org/web/2020id_/`.

## Blocked or unusable

- OpenAlex search: budget exhausted (see above). arXiv: 429 after the first batch. Semantic Scholar single GET: 429.
- Cloudflare "Just a moment" walls (not attempted past one fetch): `cris.unibo.it`, `research.rug.nl` file links. MDPI links: no PDF returned.
- `hdl.handle.net/10183/...` (UFRGS): SSL certificate chain error from this client. `elib.uni-stuttgart.de`, `digibug.ugr.es`: landing pages with no PDF link.
- `cs.purdue.edu/.../ALPS.pdf`: 404.
- Publishers (IEEE, ACM, Springer, Elsevier, Wiley, World Scientific): no OA copy found, so metadata_only.
- DBLP and CORE not tried. Unpaywall not used (needs an email). No email, key or login was used anywhere.

## Wanted but no legal open copy found (metadata_only)

Highest value among them: Rao DHT work (Rao et al., MTAF TPDS 2015; keyword content dissemination P2P 2011),
Zhao et al. reliable high-performance content-based pub/sub (JPDC 2013), HSIENA (Petroni and Querzoni), distributed event-space
partitioning (Beraldi), Salehi/Jacobsen subscription covering and ICDCS 2017 (Wayback copies found for two of them only),
Koldehofe's distributed CEP papers (DOI landing only), Cugola's mobile CBPS chapter, Tarkoma book chapter 10, the Banno apcc 2015 paper,
and the Lahyani MANET series is partly on HAL (three records found via HAL; others not).

## Seeds for other slices (deliberately not catalogued here)

- ICN/NDN/PSIRP pub/sub: COPSS (10.1109/ancs.2011.27), HoPP (arXiv 1801.03890), Carzaniga CBPS and ICN (10.1145/2018584.2018599),
  LISP pub/sub (RFC 9437), Fotiou/Gajic PSIRP papers, Moll brokerless pub/sub over NDN.
- SDN/P4 content-based networking: Wernecke et al. (10.1109/nfv-sdn.2018.8725641 and follow-ups), Kundel (10.1109/noms47738.2020.9110381),
  Jepsen packet subscriptions, Parzyjegla OpenFlow, SDN-like pub/sub (arXiv 1308.0056, Zhang and Jacobsen).
- Blockchain: HyperPubSub (arXiv 1907.03627 and 10.1145/3155016.3155018 Zupan), Trinity (arXiv 1807.03110), DPPS (10.1109/blockchain62396.2024.00019),
  truck platooning smart-contract pub/sub (10.1109/tvt.2020.3043626).
- Privacy: Tariq broker-less IBE (10.1109/tpds.2013.256, I did include it as brokerless core), Onica CPS survey (arXiv 1705.09404), Daubert anonymous pub/sub (10.1007/978-3-642-38631-2_34 area),
  Pal P3S (10.1007/978-3-642-35170-9_24), Uzunov security survey (10.1016/j.cose.2016.04.008).
- MQTT federation and distributed brokers: Detti (10.1109/tnsm.2020.3003535), Kosaka, Toyohara, Hmissi TD-MQTT, MQTT-ST (arXiv 1911.07622).
- Cloud-hosted scalable pub/sub (not decentralized): Dynamoth (10.1109/icdcs.2015.56), MultiPub, Setty cloud allocation (10.1109/icdcs.2014.63), StreamHub.
- GossipSub / Plumtree / libp2p: arXiv 2007.02754, 2507.19013 (Floodsub formalization).
- Spatial-keyword matching algorithms over a single node (Li, Chen, Hu, Wang; ICDE/TKDE 2013-2018): excluded as centralized.

## Judgement calls

- Included as `adjacent`: distributed or decentralized complex event processing (Koldehofe, DSCEP, Fardbastani, Roger), DHT range-query and attribute-tree
  indexing (Shen, Nguyen), geo/spatial distributed matching (Chen et al., Tsuruoka), DHT load-balancing survey (Felber).
- Pairs of records with the same arXiv and venue paper were merged into one record carrying the arXiv id; `year_published_venue` appears where the earliest public year differs.
