# PB6-deployed-messengers: collection log

Slice: deployed or prototyped decentralized and privacy-oriented messengers, their specifications,
audits and academic analyses, plus ledger-based private events and messages.
Catalog: `catalog/PB6-deployed-messengers.jsonl`. Files: `pdfs/` (PDF where one exists, Markdown page
text otherwise). Collection date: 2026-10-01.

## Counts

122 lines in `catalog/PB6-deployed-messengers.jsonl`: 98 `downloaded`, 11 `metadata_only`, 13 `duplicate` (pointers to PB1 or H-iog slugs). No `not_found` lines.

## How the sources were found

The usual discovery indexes were mostly unusable. Hosts and what happened:

| Host | Result |
|---|---|
| api.openalex.org | HTTP 429 on every call: "no API key, free daily budget shared by everyone on your network's IP address" exhausted. Zero OpenAlex results used. |
| api.semanticscholar.org | 429 on most queries; a few answered (usability, Freenet, SSB, Session). Used only to identify titles. |
| export.arxiv.org | Works but slow (shared lock, 3.5 s per call and heavy sharing); several queries returned 429. |
| api.crossref.org | Works. Good for DOI and author checks, poor for relevance ranking (title queries return noise). |
| eprint.iacr.org | Heavy 429 throttling for about an hour. Retried with 30 s back-off in a background loop (max 4 attempts per file per round); most PDFs eventually arrived. |
| dl.acm.org | HTTP 403 (bot wall) for the Tarr SSB paper; not circumvented, metadata only. |
| link.springer.com | Returned an HTML landing page, not a PDF (Cohn-Gordon JoC); the ePrint copy was used instead. |
| ieeexplore / xplorestaging | Paywalled (Yu and Haines, EuroS&P 2026); metadata only. |
| docs.midnight.network | Vercel security checkpoint (429); not bypassed. The Midnight ledger spec on GitHub was used instead. |
| mdpi.com | Article HTML returned no text to the helper; metadata only (Li 2025). |
| git.gnunet.org/bibliography.git, bib.gnunet.org/docs, bibliography.gnunet.org | 404 or DNS failure for CADET and GNS PDFs; metadata only. |
| duckduckgo html (through WebFetch) | refused by the tool; not tried further. |
| WebSearch | The session budget (200 calls, shared with other agents) ran out after about a dozen calls here. |

Most primary documents were located through knowledge of the projects and then fetched directly:
GitHub raw URLs and the GitHub tree API (SimpleX, Briar via code.briarproject.org GitLab API,
Matrix proposals, XMTP XIPs, Farcaster, Vac RFC index, Jami docs on git.jami.net, Ricochet Refresh),
vendor and standards sites (signal.org, whatsapp.com, spec.matrix.org, docs.autocrypt.org,
zips.z.cash, protocol.penumbra.zone, specs.namada.net, docs.aztec.network, ssbc.github.io,
toktok.ltd, berty.tech, veilid.com), conference sites (usenix.org, ndss-symposium.org) and arXiv.

Searches actually run (all for discovery; results beyond those catalogued were off-topic):
- WebSearch (about a dozen calls before the budget ran out): Session whitepaper/onion requests; Cwtch metadata-resistant; Ricochet Refresh audit;
  Matrix Albrecht vulnerabilities; Matrix Olm NCC audit; Cwtch security handbook; Session Protocol v2; Lokinet LLARP;
  Berty Wesh; Veilid routing; Autocrypt/Delta Chat audits; Tox spec; Careless Whisper.
- Crossref (about 40 title or bibliographic queries): SSB, Bridgefy, Telegram MTProto, Threema, sealed sender, decentralized
  messenger comparisons, usability, Freenet, GNUnet, Jami, Zcash memo, Penumbra, Namada, Aztec, XMTP, SoK secure messaging,
  Session, SimpleX, Briar, Tox, Delta Chat, Matrix federation, metadata leakage, WhatsApp enumeration.
- arXiv (about 40 queries, about half answered): WhatsApp metadata, Bridgefy, Scuttlebutt, Delta Chat, contact discovery, Matrix,
  Briar/Cwtch/Ricochet (physics noise only), Session onion, Zcash memo, Signal post-quantum, group messaging, GNUnet, Freenet, Veilid/Jami,
  stealth address Ethereum, XMTP/Farcaster, Nostr.
- Semantic Scholar: usability study decentralized messaging; Freenet; Secure Scuttlebutt; Session Oxen.

## What is in the catalog (by family)

- SimpleX (11 documents + 2 audits): overview, SMP, agent protocol, PQ double ratchet, XFTP, XRCP, security model, push
  notifications, chat protocol, channels protocol and overview; Trail of Bits 2022 audit and 2024 design review.
- Session (8): arXiv whitepaper, Session docs on onion requests and swarms, Protocol V2 design post, Lokinet LLARP design page, Quarkslab audit,
  a TUM seminar analysis; WOOT 2026 attacks paper (downloaded); EuroS&P 2026 attacks paper (metadata only).
- Briar (5 Bramble protocol specs + Cure53 pentest), Cwtch (whitepaper + three handbook pages), Ricochet (design, protocol v3, NCC audit),
  Tox (spec), Jami (swarm/DRT docs), Berty (Wesh protocol), Veilid (launch slides), Secure Scuttlebutt (protocol guide; ICN paper metadata only),
  Delta Chat / Autocrypt (Autocrypt spec 1.1.0, USENIX Security 2024 analysis, three audits), GNUnet (P4T paper; CADET and GNS metadata only),
  Freenet/Hyphanet (three metadata-only records).
- Matrix (13): federation API, Olm and Megolm specs, four MSCs (state resolution, v2.1, history sharing, cross-signing),
  NCC Olm review, Albrecht et al. S&P 2023, DOGM formal analysis, ProVerif analysis, Jacob et al. scalability.
- Signal, WhatsApp and other mainstream analyses: X3DH, Double Ratchet, PQXDH, Sesame, ML-KEM Braid specs; Cohn-Gordon,
  Alwen et al., Rosler et al. (group chats), Balbas et al. (Sender Keys), Dodis et al. (Triple Ratchet), Bhargavan et al. (PQXDH),
  Chase et al. (private groups), Malvai et al. (key transparency), WhatsApp white paper, Martiny et al. and Brigham/Hopper (sealed sender),
  Hagen et al. and Gegenhuber et al. (contact discovery, delivery receipts, account enumeration), Paterson et al. (Threema),
  Albrecht et al. (Telegram; Bridgefy twice).
- Ledger-based channels: Zerocash, Zcash protocol spec (duplicate), ZIP 302/231 (memo), ZIP 307 (duplicate), Kappos et al. (measurement),
  Penumbra detection keys and FMD, Namada MASP, Midnight Zswap ledger spec, Aztec private events and note tagging, BIP 47 / BIP 352,
  ERC-5564 plus BaseSAP and Kovacs-Seres Umbra measurement, Cardano CIP-20 and CIP-83, Whisper EIP-627 (duplicate),
  XMTP XIPs 42/46/49, Farcaster protocol spec, Waku core specs (all duplicates of PB1) and Noise sessions.

The `note` field of each record states what the system hides (sender, recipient, content, relationship, timing) and what it leaks.
Reliability of those statements differs. They were checked against the abstract or executive summary for all papers and audits
(SimpleX audits, Quarkslab, Cure53, NCC, Matrix papers, Martiny, Telegram, Careless Whisper, Zcash/ZIP 307 and Penumbra pages, Aztec docs, Berty spec,
Briar BTP/BRP, SSB guide, Veilid slides). For the SimpleX, Cwtch, Tox, Autocrypt, Jami and Farcaster specs the hide/leak
statements follow the documents' stated goals and a keyword-level reading, not a line-by-line review; verify before quoting in the review.

## Overlap with other clusters (the lead should deduplicate)

- PB1-bitmessage-heirs already has the Waku RFCs, Whisper EIP-627, Zcash protocol spec, ZIP 307, Penumbra FMD page, Nostr NIPs, BIP 47,
  Bridgefy (2021) and Umbra measurement. The PB6 lines for those are `duplicate` and carry the PB1 slug, except two where both clusters
  used the same slug and file and both lines are `downloaded`: `2021-berty-wesh-protocol` and `2023-kovacs-umbra-anonymity`.
- PB6 line `2015-bip47-payment-codes` is a real download; PB1's slug `2015-bip47-paymentcodes` is itself marked duplicate of something else,
  so two copies of BIP 47 exist in `pdfs/`.
- Hagen et al. (contact discovery) is also under PB2 as `2021-hagen-allnumbersus` (duplicate). PB6 holds the real file.
- Kachina and Zswap are catalogued by H-iog; PB6 has `duplicate` pointers only.
- `2021-martiny-sealed-sender.pdf` and `2021-martiny-sealedsender.pdf` are the same file (another cluster downloaded it as well).
- `2022-penumbra-protocol-detection-memo.md` overlaps PB1's Penumbra FMD page but covers addresses, detection keys, memos and note ciphertexts as well.

## Wanted but not obtained

- Tarr, Lavoie, Meyer, Tschudin, SSB ICN 2019 (ACM 403). Kermarrec, Lavoie, Tschudin, "Gossiping with Append-Only Logs in Secure-Scuttlebutt" (DICG 2020): found as a title only, no record written.
- Yu and Haines, "Practical Attacks on Session Messenger and Oxen Blockchain" (EuroS&P 2026, IEEE paywall).
- Polot and Grothoff, CADET (2014) and Wachs et al., GNS (CANS 2014): PDFs 404 at the GNUnet bibliography.
- Roos et al. (Freenet measurement, PETS 2014), Roos and Strufe (dead ends), Clarke et al. (Dark Freenet, 2010): no open PDF located.
- Terzo, Cremers, Gonzalez et al., "Formal Security Analysis of the Olvid Messenger" (IACR ePrint 2026/1622, CCS 2026): abstract page read, PDF fetch kept returning 429, so the record is metadata only.
- Push Protocol (chat/notifications) whitepaper: only a Push Chain litepaper was found, which concerns the Push chain, not the messaging protocol; not catalogued.
- Lokinet / Loki whitepaper PDF, Status whitepaper, Jami or Tox academic analyses, Olvid and Wire protocol documents, Signal "Private Contact Discovery" write-up, Apple iMessage PQ3 analysis, Hyphanet Freemail/FMS documents: not located or not attempted after the index failures.
- Midnight documentation pages (docs.midnight.network) and the Aztec yellow paper: not fetched (checkpoint; time).
- Cwtch Tapir and group pages, Session protocol pages beyond onion requests and swarms: only the pages listed above were saved.
- Studies that compare many decentralized messengers directly (usability, traffic analysis, metadata) are scarce in what the available indexes surfaced:
  only Li 2025, Sheoran 2026 (synthetic data, low evidence) and Saha et al. 2026 (title only) were found, all metadata only.

## Seeds for other slices

- Key transparency lineage (CONIKS, SEEMless, Parakeet follow-ups) and Meta's AKD; Apple iMessage PQ3 and its formal analysis (Linker, Sasse, Basin).
- Bridgefy-style mesh messaging attacks: Perry, Spang, Eskandarian, "Strong Anonymity for Mesh Messaging" (arXiv 2207.04145) is already in PB1/PB2.
- Olvid (French messenger without phone numbers) analysis: ePrint 2026/1622 (see above).
- Messaging Layer Security: RFC 9420, RFC 9750 and analyses (XMTP and others build on MLS); catalogued by H-iog only through two IOG papers.
- Signal's SPQR: Triple Ratchet (collected here), ML-KEM Braid spec (collected here); the PQ3 and Signal comparison papers should be read together.
- Fuzzy message detection, oblivious message retrieval and private signaling are held by PB1/PB2; Aztec's tag scheme and Penumbra's detection keys here are the deployed counterparts.

## Observations useful for the review

- Recipient privacy mechanisms seen in deployed systems fall into four types: public flood with trial decryption (Whisper, SSB private-box, Zcash/Penumbra/Namada/Midnight notes, ERC-5564, BIP 352), per-pair random addresses on relays (SimpleX queues, Briar rendezvous, Berty rendezvous points, Waku content topics), public per-recipient mailboxes on a small node set (Session swarms), and rolling tags (Aztec note tags, Waku/Noise topics).
- Source anonymity is the weak part of nearly all of them. Sealed sender is defeated by statistical disclosure through delivery receipts (Martiny et al.; Brigham and Hopper extend it to groups); Careless Whisper and WhatsApp enumeration leak device state and registration through receipts and directories. SimpleX's 2024 design review (Trail of Bits) found user-correlation channels.
- Custom protocols dropped the Signal ratchet and paid for it: Session V1 has no forward secrecy and no mutual key authentication (Session V2 design post; Urushigaki et al. WOOT 2026); Matrix's Megolm trades FS and PCS for history sharing (Albrecht, Dowling, Jones); Bridgefy's libsignal adoption was not enough (Albrecht, Eikenberg, Paterson).
- Ledger channels hide content and relationships but expose existence, time, fees and (for stealth addresses) funding links; empirical studies show large losses (Kappos on Zcash shield/unshield flows; Kovacs and Seres on Umbra: recipient identified for 25.8 to 65.7 percent of payments depending on chain).

## Final counts

98 downloaded (47 PDFs and 51 Markdown page or spec texts), 11 metadata_only, 13 duplicate; 0 not_found.
