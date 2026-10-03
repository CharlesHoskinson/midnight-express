# PB4-source-anonymity-spam: collection notes

Slice scope: (a) source anonymity in P2P flooding and gossip, (b) network-level attacks on P2P overlays,
(c) anonymity networks as transport, (d) anti-spam and admission control. Collected 2026-10-01.

## Counts

134 catalog lines in `catalog/PB4-source-anonymity-spam.jsonl`.

| status | count |
|---|---|
| downloaded (PDF or Markdown copy in `pdfs/`) | 104 |
| metadata_only (no legal open copy reachable) | 11 |
| duplicate (another slice already holds a copy; my copy removed, my adversary note kept on the line) | 19 |
| not_found | 0 |

Roles: attack_or_audit 43, building_block 41, system 21, measurement 15, limit_or_theory 13, sok_or_survey 1.
Background (pre-2012) items: 4 (Douceur, Back, Laurie and Clayton, Liu and Camp).
The `note` field of every line starts with what the source does and then states the adversary model
("Adversary: ...") of the attack or defence. `cited_by` is null throughout: OpenAlex was rate limited
(see below), so no citation counts were collected.

## Queries and routes used

OpenAlex was almost unusable. Every `api.openalex.org` request answered 429 for long stretches because
other collection agents share the same unauthenticated pool; two title-lookup batches of 20 to 30 titles
returned only a handful of hits (see the `found_via: openalex` lines). arXiv's Atom API (`export.arxiv.org`)
was slow (60 s timeouts, repeated 429) for the same reason. So most records come from known titles checked
against the PDF first page (`pdftotext`, title must match) rather than from search.

arXiv API queries (title and abstract phrases): rumor source obfuscation; anonymity in the Bitcoin P2P
network; Dandelion AND bitcoin/anonymity/transaction; Clover; first-spy; Monero AND Dandelion++; Zcash AND
deanonymization; anonymous broadcast AND lower bound; Ethereum validators AND anonymity; eclipse AND Ethereum;
Hijacking Bitcoin; Erebus; TxProbe; Basalt; GossipSub; Sybil AND SoK; Waku; rate-limiting nullifier;
Privacy Pass; Counter-RAPTOR; AS-level adversaries Tor; Tik-Tok, Var-CNN, website fingerprinting variants;
Coconut; zk-promises; Sybil AND Tor; Honey onions; Walking Onions; I2P AND anonymity; contact discovery;
DeepCoFFEA; rumor centrality; gossip AND anonymity (this found "On the Inherent Anonymity of Gossiping");
Lightning privacy; Nostr relays; eclipse AND countermeasures. Several of these returned nothing or timed out
(`Metadata-conscious anonymous messaging`, `rumor source obfuscation on irregular trees`, Triplet
Fingerprinting, Counter-RAPTOR search, Walking Onions, DeepCoFFEA, Gupta-Saia-Young resource burning, Safely
Measuring Tor): they were not searched again, so absence from the catalog is not evidence of absence.

Direct-URL routes that worked: arXiv PDFs, USENIX Security PDFs, NDSS PDFs (found by scraping the
`ndss-symposium.org/ndss-paper/` landing page for the `.pdf` href), PoPETs, IACR ePrint (works but hit 429
bursts), HAL (Inria), author pages (ohmygodel.com, robgjansen.com, princeton.edu/~pmittal, cl.cam.ac.uk),
freehaven.net/anonbib cache, IETF datatracker and rfc-editor.org, `lip.logos.co` (the Logos LIP site; the
old `rfc.vac.dev` URLs now return a "Page not found" page with a 200 status, so the first save of the
WAKU2-RLN-RELAY spec was a false positive and was deleted), raw GitHub files (BIP 156, NIP-13, libp2p
GossipSub v1.1, Tor torspec proposals), `spec.torproject.org` (only the vanguards page has real text on its index
page; the hspow and rend-spec index pages are stubs, so I used torspec proposals 327 and 224 instead).
Markdown copies of web specs had navigation boilerplate; email addresses in them were replaced by
`[email omitted]`.

## Hosts that blocked or failed

- `dl.acm.org` (403 on PDF download), `pubs.aeaweb.org` / `www.aeaweb.org` (403), IEEE Xplore (paywall, no
  attempt): the corresponding items are metadata_only. No attempt was made to get around any of them.
- `orbilu.uni.lu`: TLS certificate chain does not validate locally ("unable to get local issuer certificate").
  I did not disable verification; the Biryukov and Tikhomirov paper is therefore metadata_only although an
  open copy exists there (the OpenAlex hit gave `https://orbilu.uni.lu/bitstream/10993/39724/1/biryukov-tikhomirov-deanonymization-and-linkability.pdf`).
- `ro.uow.edu.au` (BLACR): 403. `primecoin.io`: 404. `muoitran.com`: no paper link. Semantic Scholar: 429.
- WebSearch budget (shared, 200 calls) was exhausted before the second half of the run; later gaps are due to that.

## Wanted but not obtained (metadata_only)

- Biryukov and Tikhomirov, Deanonymization and linkability of cryptocurrency transactions (EuroS&P 2019, Bitcoin and Zcash): open PDF exists at orbilu, certificate error.
- Tran et al., Erebus / A stealthier partitioning attack (S&P 2020): IEEE only.
- Kim et al., Measuring Ethereum network peers (IMC 2018): ACM 403.
- Alvisi et al., SoK: evolution of Sybil defense via social networks (S&P 2013): IEEE only.
- Egger et al., Practical attacks against the I2P network (RAID 2013): Springer only.
- Rao and Reiley, The economics of spam (JEP 2012): AEA 403 (the article is open access on AEA; try a browser).
- King, Primecoin whitepaper (2013): original URL gone.
- Dyer et al., Peek-a-boo, I still see you (S&P 2012): author URL 404.
- Au, Kapadia and Susilo, BLACR (NDSS 2012): repository 403.
- Lee et al., Anon-Pass (S&P 2013): IEEE only.
- Fanti et al., Metadata-conscious anonymous messaging (IEEE TSIPN 2016): no arXiv or open copy located.

Never located at all (no catalog line): Koshy et al., An analysis of anonymity in Bitcoin using P2P network
traffic (FC 2014); Shah and Zaman, Rumors in a network: who's the culprit (2011); Walking Onions
(Komlo, Mathewson, Goldberg 2020); Triplet Fingerprinting (CCS 2019; arXiv id 1902.06421 is Tik-Tok, not Triplet);
DeepCoFFEA (S&P 2022); Gupta, Saia and Young on Sybil defence by resource burning; Oya et al. "Do dummies pay
off?" (PETS 2014); Das et al. "Comprehensive anonymity trilemma" (2020); any Kovri/I2P-specific Dandelion++
analysis (none found; the Monero material is Shi et al. NDSS 2025 on eclipse and Shi et al. 2026 on Tor
transport deanonymisation); any Zcash-specific network-layer paper other than Biryukov and Tikhomirov.
Clover has no confirmed peer-reviewed venue, so it is listed as an arXiv preprint.

## Duplicates with other slices

19 lines have `"status":"duplicate"`: the PDF was already in `pdfs/` under another slice's slug (C, PB1, PB2,
PB6, PB7), so my copy was removed and the line carries the existing slug in `slug` and `duplicate_of`, with my
adversary-model note kept. Conversely PB7 has marked several sources as duplicates of files I downloaded
under this slice's slugs (Dandelion, Dandelion++, adaptive diffusion, Fanti and Viswanath, Sharma et al.,
Ando et al., Johnson et al., Biryukov trawling, Hoang I2P); those PDFs stay under PB4 slugs and the PB4
lines are the canonical records, so do not drop them in the merge.

## Adversary-model map (what the notes show)

Source anonymity in flooding (a):
- First-spy / supernode adversary: one well-connected passive node, or a fraction p of colluding spies,
  that records first receipt (Biryukov et al. 2014; Fanti and Viswanath 2017; Biryukov and Tikhomirov 2019).
  Flooding and diffusion give poor anonymity against it; Dandelion/Dandelion++ and Clover add a stem or proxy
  hop to defeat it.
- Snapshot / rumor-centrality adversary: sees the infected set at one time (Fanti et al. adaptive diffusion).
- Active or protocol-deviating spies (Dandelion++ is designed for them, Dandelion is not).
- Evaluation against these: Sharma et al. (NDSS 2023) find none of Dandelion, Dandelion++ or Lightning
  gives acceptable anonymity (colluding fraction 1 to 15 percent); Guerraoui et al. (DISC 2023) give a
  differential-privacy limit (poorly connected graphs admit no gossip protocol with meaningful anonymity).
- Structure leaks: validator-to-IP linkage from subnet duties in gossipsub (Heimbach et al.); Tor-proxy
  forwarding pattern in Monero (Shi et al. 2026); stem relays without validation open a DoS channel
  (Tabatabaee et al.).

Overlay attacks (b):
- Eclipse needs IP resources and a peer-table weakness: many IPs (Heilman 2015), two hosts (Marcus 2018,
  Henningsen 2019), DNS-list and slot hijack (Shi 2026), connection reset (Shi, Monero NDSS 2025), AS-level
  position (Erebus), BGP (Apostolaki). Defences: bucketed address tables, feelers, peer scoring (GossipSub 1.1),
  Byzantine-resilient peer sampling (BASALT), client-side detection (Alangot et al.).
- Topology inference as a precursor: TxProbe, Neudecker et al.

Anonymity networks as transport (c):
- End-to-end correlation adversaries (relay-level, AS/IXP, BGP) against Tor: Johnson et al., Raptor, DeepCorr, Early-MFC.
- Local passive observer: website fingerprinting and its defences (k-FP, Deep Fingerprinting, Tik-Tok, WTF-PAD, Walkie-Talkie, FRONT).
- Onion-service specific: HSDir enumeration and snooping (Trawling, Honey onions), guard discovery
  (Vanguards proposals), circuit fingerprinting (Kwon), long-lived introduction circuits (Constantinides 2026).
- I2P: Egger (metadata only), Hoang, Timpanaro, Wang 2025, Akanbi 2025.
- Messenger metadata: Conti (user actions), Careless Whisper (delivery receipts), contact discovery (Hagen).

Anti-spam and admission control (d):
- Cost-based: Hashcash, Laurie and Clayton (PoW cannot separate spammers because botnets are free), Liu and
  Camp (reputation-scaled difficulty), Rao and Reiley (economics), Equihash/Argon2/scrypt/Balloon (memory
  hardness), proofs of space and of useful work, SybilControl, Nostr NIP-13, Whisper (EIP-627), Tor PoW for onion
  introduction (proposal 327, dynamic effort).
- Credential-based: Privacy Pass (paper and RFCs 9576 to 9578, OPRF 9497, blind RSA 9474), ARC, ACT, BBS,
  Coconut, KVAC (Chase et al.), anonymous tokens with private metadata bit, zk-promises (anonymous reputation
  and revocation), BLACR, Anon-Pass.
- Stake and rate-limit based: RLN v1/v2, Waku RLN-relay (+ latency paper), mixnet DoS protection and
  multi-message burn RLN specs.
- Accountability for abuse in E2EE: message franking (Grubbs; Tyagi is a duplicate of PB2).

## Seeds for other slices

- IACR/ePrint: "Comprehensive anonymity trilemma" (Das et al.), Gelernter and Herzberg limits (held by PB7).
- Walking Onions, Triplet Fingerprinting, DeepCoFFEA and Gupta-Saia-Young Sybil defence (not found; re-query once OpenAlex recovers).
- Cover traffic and constant-rate flooding in gossip pub/sub (no direct hit found); a targeted query on
  "cover traffic" with "Waku mix" or "gossipsub" in OpenAlex would be worth running.
- Dandelion in other chains: Grin, Beam (one DoS paper found), Zcash network-layer attacks, Ethereum
  privacy-enhanced routing (ethp2psim found; its parent proposals are not catalogued).
- Nostr measurement papers (Wei and Tyson 2024, arXiv 2402.05709) appeared in a search and were not added; they fit a relay-based pub/sub slice.
- BIP 324 follow-ups and the Bitcoin Core addrman/anchor-connection changes (design notes, not papers).
