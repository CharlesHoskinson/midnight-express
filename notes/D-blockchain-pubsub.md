# D-blockchain-pubsub: collection notes

Scope: blockchain-, ledger- and smart-contract-based pub/sub and event systems (2014-2026), oracles as outbound
event paths, cross-chain relays, ledger-backed MQTT, decentralized social-feed protocols.

Result: 81 records in `catalog/D-blockchain-pubsub.jsonl` (35 core, 46 adjacent); 26 downloaded, 55 metadata_only, 0 not_found.

## Sources and what worked
- OpenAlex: 18 of ~75 planned queries ran (about 630 raw hits, 59 title-relevant) before the shared free daily budget
  ran out (HTTP 429 with "Insufficient budget", reset at midnight UTC). The remaining ~55 OpenAlex queries were NOT run.
- Crossref: ~90 query variants (bibliographic and free-text), title filtered by hand. Good for DOIs, authors, venues; noisy ranking.
- arXiv API: ~70 queries; several 429/503 under shared load. Titles looked up by `ti:` for every metadata_only record: one extra copy found (Chervinski).
- Semantic Scholar: search was throttled hard (about 17 of 70 queries finished). Citation endpoints worked and were the best
  source: forward citations of 27 seeds (Trinity, HyperPubSub x2, Hashemi, Lv, Zhao, Ghaemi, BPS, Galaxy, DPPS, Kleppmann,
  Balduf, Raman, Mastodon, Matrix, Muhlberger, Pasdar, Hull, and others). `paper/batch` gave OA links and abstracts.
- WebSearch was unavailable (session budget used up).
- Hosts that blocked or refused: MDPI (200 HTML wall instead of PDF), Hindawi downloads (403), Europe PMC render (520),
  dl.acm.org PDFs, ScienceDirect PDFs, ieeexplore PDF links without a direct OA arnumber. Not bypassed; those records are metadata_only
  and keep the publisher link. DBLP, CORE and Unpaywall were not used.

## Dedup
Skipped because another slice already holds them: Topiary, GossipSub papers, Waku family, SmartPubSub, Pulsarcast (C-gossipsub-libp2p);
Nostr empirical, Nostr attacks (PB1); VAST, SELECT, Tryfonopoulos, Decentagram (A-gossip-topic); Alam interoperability verification,
DPPS, Gajji, Tong DAIoTtalk, Park content sharing, Abegg minimum-encryption (G-surveys-citations); Marzal (F-edge-iot-icn);
Spohn "Publish, subscribe, and federate!" (B-dht-content); Tarr SSB (PB6); Zamyatin SoK (H-iog). Records for these are in the owning slice.

## Core findings
Blockchain-as-broker line: Zupan HyperPubSub (Middleware 2017, Hyperledger, metadata only), Hashemi (2017), Zhao Secure Pub-Sub (2018), Trinity (2018/2019),
Bu HyperPubSub (SRDS 2019), Lv (Access 2019), Huang BPS (2020), Abegg SUPRA (2021), Galaxy (2023), DPPS and ZK-DPPS (2024), VMC2-PS (2025).
Pub/sub as chain interoperability layer: Ghaemi (2021), Alam (2023, in G). Notification proofs: Behl (2021), Signet (ICDCS 2026).
MQTT plus blockchain: roughly 15 mostly low-citation papers; most use the chain for authentication or broker failover, not for dissemination.

## Wanted but not obtained (no legal open copy found)
Zupan HyperPubSub (ACM), Zhao Secure Pub-Sub (IEEE Access gold OA but PDF link not reachable by script), Huang BPS (JPDC), Galaxy (IoT-J),
Xing truck platooning, Liu multi-domain (Hindawi, 403), Ataei (MDPI wall), Buccafurri MQTT OTP (MDPI wall), Idrees smart broker (MDPI wall),
Signet, Hull DEBS 2017, Ye "Behind Farcaster", SegSub, Agostinho MQTT-Chain, Kostler SmartStream, Pateria, Kaleem (ACM).

## Gaps and seeds for other slices
- Decentralized social feeds are thin: no Lens, Farcaster-hub, or Matrix-federation dissemination paper beyond Ye 2026 (metadata only) and Raman/Jacob/Kleppmann/Balduf.
  Rerun OpenAlex for "Farcaster", "Lens Protocol", "Matrix federation", "ActivityPub delivery", "AT Protocol relay" after the budget resets.
- Not run: OpenAlex queries on payment channels, token-incentivised pub/sub, IOTA, Waku/Whisper/Swarm PSS, XMTP/Push notification protocols,
  Ethereum event-log indexing (The Graph), Chainlink OCR, IBC.
- The oracle literature is large (hundreds of papers); only items framed as inbound/outbound or pub/sub patterns were kept
  (Muhlberger, Pasdar x2, Al Breiki, Caldarelli, Town Crier, DAON). A dedicated oracle slice would need a separate inclusion rule.
- Possible seeds: Chervinski cross-chain messaging cites for relayer designs; Kaleem EDSC for event-driven contract platforms;
  Jabbari/Ramachandran DPPS group for further BFT pub/sub work.
- Note texts for metadata_only records were written from titles and abstracts only, not full texts.
