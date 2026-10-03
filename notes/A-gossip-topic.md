# Slice A-gossip-topic: notes

Catalog: `catalog/A-gossip-topic.jsonl` (194 records: 136 core, 58 adjacent; 57 downloaded, 137 metadata_only, 0 not_found).

## What blocked the run (read this first)

- **OpenAlex is exhausted for the day.** After about 40 requests the shared-IP free budget hit zero
  (429, "Insufficient budget ... resets at midnight UTC", retry-after about 8 h). No email or key was used.
  So the planned `cites:` forward-citation sweep ran only for 4 seeds through OpenAlex
  (PolderCast W2164114419 / Vitis W2097943705 + W1485579857 / SpiderCast W2107233660 = 3 pages of 100 max each).
  The rest of the forward-citation work used **OpenCitations COCI** (DOI to citing DOIs, no key) plus
  **Crossref** metadata. COCI covers only DOI-to-DOI links, so it misses arXiv-only and non-Crossref citers.
- **Semantic Scholar**: 429 on single calls; the `POST /paper/batch` endpoint worked (about 175 DOIs for
  `openAccessPdf`), after one 429 and a 35 s back-off. Used for OA PDF URLs only.
- **arXiv API** (export.arxiv.org): answered at first, then 429 for the rest of the session. Metadata for the
  arXiv-only items came from Semantic Scholar.
- **DiVA (kth.diva-portal.org, urn.kb.se)**: connection reset from this client on every attempt. Not retried
  beyond three tries. Affects Vitis (KTH copy), Rahimian theses, BeaConvey KTH copy.
- **UiO NORA/DUO handles** (`hdl.handle.net/10852/...`) now redirect to a JS app (nva.sikt.no); no PDF link reachable.
- **MDPI, Hindawi, ACM, IEEE, ScienceDirect, Springer**: bot walls or paywall; not attempted past one try.
  Those records are `metadata_only`.
- **msrg.org** (Jacobsen group, Toronto): the old `publications/pdf_files/` URLs now 404. Papers there were
  fetched from the **Internet Archive** copy of the author-hosted PDF (`web.archive.org/web/2020id_/...`),
  located with the Wayback CDX index. Chen/Vitenberg/Jacobsen overlay-design papers, Publiy, Muthusamy ToN, Zhang top-k
  all came this way. This is the authors' own open PDF, not a paywall bypass.
- WebSearch budget for the session was already spent, so no web-search discovery was possible.

## Queries run

- OpenAlex: 3 search queries (PolderCast, Vitis, SpiderCast) + `cites:` on 3 seed IDs, 1 title lookup for Vitis.
- OpenCitations COCI citing-DOI lists for 24 seeds in wave 1 (PolderCast, Vitis, SpiderCast, TERA, Magnet, BlueDove,
  Onus-Richa, Chen ICDCS11, Rahimian locality, Matos TPDS, XL survey, Ferretti, Feverfew, Spotify, Teranishi,
  Tariq, community clustering, Chen D&C, GenODA, Onus 2015, WTCO, Ding, PAPaS, PopSub, Salehi) and 67 core
  records in wave 2 (about 580 citing DOIs in total, 176 new in wave 2; wave 2 added almost nothing in scope).
- Crossref `query.bibliographic` (from 2011), about 26 queries: topic-based p2p overlay, gossip pub/sub,
  topic-connected overlay, decentralized rendezvous, interest clustering, epidemic dissemination, DHT content-based,
  social pub/sub, small-world relay, min topic-connected overlay, low-diameter, subscription clustering, peer sampling,
  Scribe-style rendezvous, hybrid structured/unstructured, self-organizing, brokerless, serverless event notification,
  churn, epidemic multicast, fog/edge p2p, surveys, fairness, locality. Crossref fuzzy ranking is noisy; results were
  filtered by title keywords and read by hand.
- arXiv: about 15 phrase queries (before the 429 wall).
- HAL API title match for all records without a PDF (7 hits).

## Scope calls

- Kept the whole **Nakamura / Nakayama / Saito / Enokido-Takizawa "P2PPS"** line (about 40 papers; protocols for
  information-flow control, causal ordering and fog variants in peer-to-peer topic-based pub/sub). They cite PolderCast,
  are P2P pub/sub, and are mostly Springer/IEEE (metadata_only). The lead may want to down-weight them.
- Kept the **topic-connected overlay (TCO)** theory line (Onus-Richa, Chen et al., Hosoda et al., Steinova et al.) and
  the graph-theory restatements (Subset Interconnection Design, Minimum Connectivity Inference, F-overlay, hypergraph
  support): tagged `adjacent` for the pure combinatorics.
- Dropped as out of scope or not pub/sub: DISC-style SDN pub/sub (SDNPS, PLEROMA, SDN-like, Bhowmik), Big Active Data,
  content-matching algorithm papers (REIN, BE-Tree family, Ma et al.), cloud matcher papers except BlueDove,
  Kafka-based work, ThingsJS, Loquat, a SC poster on supercomputer membership (OpenAlex title "Poster"), Tarkoma
  chapter duplicates (kept the book).
- **Pre-2011 seeds are not in the catalog** (year rule): SpiderCast (PODC/DEBS 2007, 10.1145/1266894.1266899),
  TERA (DEBS 2007, 10.1145/1266894.1266898), Magnet (DEBS 2010, 10.1145/1827418.1827456), Sub-2-Sub, Quasar, StAN.
  Their post-2011 citers were swept via COCI. StAN and "Ace" could not be identified in OpenAlex/Crossref
  (no match for either title); open gap.
- BlueDove (IPDPS 2011) is a cloud matcher-server design; kept as `adjacent` because it was named in the brief.

## Overlap with other slices (skipped here, already in catalog/*.jsonl)

Topiary (2023), GossipSub (Vyzovitis 2020), Pulsarcast (2021), SmartPubSub (2022), Floodsub formalization (2025),
CliqueSensus (2025), Broadcast Mechanisms survey (2026). My duplicate PDFs for Topiary, GossipSub, SmartPubSub and
Floodsub were deleted; the other slice's copies stand. Matching was by DOI, arXiv id and normalized title at assembly time;
slices written later may still duplicate mine.

## Wanted but no legal open PDF found (core)

- Vitis (IPDPS 2011) and the Rahimian theses 2011/2014 (DiVA unreachable); Setty thesis 2015 and Hysenaj 2014 (UiO).
- The Hidden Pub/Sub of Spotify (DEBS 2013); Setty INFOCOM 2014 satisfied-subscribers paper (UiO copy not reachable).
- Onus-Richa ToN 2011 and Comp. Networks 2015; Tariq et al. DEBS 2012 spectral clustering (Groningen hdl returned a landing page);
  Turau ICDCS 2017; Teranishi/Banno group papers; DYNATOPS; GraPS; DEBS/ICDCS/Middleware papers from IEEE/ACM.
- Oztoprak TD-CD-ODA (the AXSIS repository returned a cookie-policy PDF; discarded).

## Seeds for other slices / follow-up

- When OpenAlex resets (midnight UTC), rerun `filter=cites:` on: PolderCast W2164114419, Vitis W2097943705,
  Onus-Richa W2124124285, Chen W2165303722, Matos W2052324145, XL survey W1993437872, Turau W2735768333,
  Teranishi W2290599697, DYNATOPS W1996607820, Feverfew W2090872316, OpenPubSub W4220785404, Topiary W4389713876.
  That should catch arXiv-only and post-2023 citers COCI misses.
- Broker-mesh / SDN / DHT-based content pub/sub items seen but not collected (belong to broker or DHT slices):
  Pyracanthus, Chaabane DHT pub/sub, Yoon et al. HA broker overlays, Salehi delivery guarantees, Hyperpubsub, Trinity
  (BFT blockchain pub/sub), Decentagram (included here), MQTT federation work (Detti, Kawaguchi, D-MQTT), NDN/ICN pub/sub
  (COPSS, Coexist, Moll), Yoon "Secret forwarding" privacy paper.
- Records whose OpenAlex title was truncated were replaced by the Semantic Scholar full title. Some `venue` values are
  OpenAlex source names ("Lecture notes in computer science") rather than the conference name.
- The slugs are auto-generated (year-surname-two title words); `2012-setty-poldercast` and `2011-rahimian-vitis` were set by hand.
