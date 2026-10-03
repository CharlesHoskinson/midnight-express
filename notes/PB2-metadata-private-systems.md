# PB2-metadata-private-systems: collection notes

Slice: designed systems for metadata-private messaging and anonymous broadcast, 2012 to 2026
(DC-net, mixnet, PIR, trusted-hardware systems, plus the proofs, attacks and measurements around them).
Catalog: `catalog/PB2-metadata-private-systems.jsonl` (126 lines).

## Result counts

| status | lines |
|---|---|
| downloaded (PDF, or Markdown for web pages) | 122 |
| metadata_only | 1 (Sabre, IEEE S&P 2022) |
| duplicate (another slice already holds it; line carries that slice's slug) | 3 |
| not_found | 0 |

By role: system 69, building_block 27, attack_or_audit 11, limit_or_theory 10, sok_or_survey 5, measurement 4.
By relevance: core 64, adjacent 62. Background (pre-2012): 3 (Sphinx 2009, Herbivore 2003, Dissent CCS 2010).

`cited_by` is the Crossref `is-referenced-by-count` on 2026-10-01 and is `null` where the item has no DOI
(USENIX, arXiv-only, ePrint-only and specification items). OpenAlex counts were not available (see below).

The `note` field of every system record starts with "Cost model:" and gives bandwidth per user, latency, users
supported and the trust assumption wherever the paper states them. Numbers were read from the paper's abstract or
evaluation text, not from memory. Where a paper gives no figure the note says so. For a cross-check of all four
families, use `2023-sasy-sokmetadata` (SoK on 31 systems).

## How the slice was built

1. Seed list from the brief (Dissent, Verdict, Riffle, Riposte, Vuvuzela, Alpenhorn, Stadium, Karaoke, Atom, XRD, Loopix,
   Nym, Katzenpost, HOPR, Express, Clarion, Echomix, Sphinx, Pung, Talek, Addra, Groove, Spectrum, Blinder, contact
   discovery). Direct publisher URLs were tried first (USENIX, PoPETs, NDSS, arXiv, ePrint, institutional pages).
2. About 60 topic web searches (system names, "differential privacy mixnet", "n-1 attack", "Nym measurement", "SGX
   messaging", "PIR messaging", "Sphinx update", "contact discovery"), until the shared session cap of 200 searches ran out.
3. ePrint site search through WebFetch (queries: Sabre, Pulsar, metadata-hiding, anonymous broadcast, mixnet,
   private messaging PIR, oblivious message retrieval, dining cryptographers, private signaling, metadata-private,
   Sphinx packet format). This was the most productive discovery step late in the run.
4. arXiv API sweeps (metadata-private messaging, mix network messaging, anonymous broadcast, mixnet cover traffic,
   PIR plus anonymous communication, anonymous microblogging, oblivious message retrieval). Several returned 429 and
   were not repeated.
5. Crossref (`/works/{doi}` and `query.bibliographic`) to confirm DOIs and take citation counts. Every DOI in the
   catalog was checked against the Crossref title; several DOIs were added from Crossref (S&P, NDSS, PoPETs, ACM).
6. Every downloaded PDF was checked by reading its first page text against the catalogued title. Four wrong
   downloads from guessed ePrint ids (Clarion, Express, and Riposte three times) were deleted and refetched with the
   correct source. Final pass: no title mismatches.
7. Katzenpost specifications were taken from the project's own PDF export (`katzenpost.network/docs/specs/pdf/`).
   They carry no dates; the year in the catalog is an estimate and is flagged in each `note`.
   The Signal contact-discovery post was saved as Markdown (`pdfs/2017-marlinspike-signal-private-contact-discovery.md`)
   after checking the page text is the full article.

## Hosts that blocked or limited me

- OpenAlex: HTTP 429 from the first call. The message said the free daily budget shared by the network address was
  used up (resets at midnight UTC, about 8 hours). I did not use it. No OpenAlex ids or counts in this slice.
- WebSearch: the shared session cap (200) was reached partway through; later discovery used WebFetch on ePrint search and the arXiv API.
- eprint.iacr.org and export.arxiv.org: intermittent 429 caused by the other collectors. Failed fetches were retried
  after 60 s and 90 s; five items needed a second pass.
- IEEE Xplore (`iel8/.../11023277.pdf`): returned HTTP 202 with no PDF. Not pursued.
- zoo.cs.yale.edu (Herbivore): 403. A Cornell copy worked.
- publications.cispa.saarland: JavaScript landing pages with no direct PDF link; used the authors' MPI-SWS copies for Aqua and Herd.
- DBLP and CORE: not tried (known to be blocked).

## Wanted but not obtained

- Sabre: Vadapalli, Storrier, Henry, "Sender-Anonymous Messaging with Fast Audits", IEEE S&P 2022. No open copy found (not on ePrint or arXiv). Metadata-only record; landing page `ieeexplore.ieee.org/document/9833601/`.
- "Pulsar" (named in the brief): no paper found. ePrint's only "Pulsar" is a diffusion-model steganography paper (2023/1758); other hits are Apache Pulsar and a Nostr chat app by an independent developer. Not catalogued. If it is a specific recent PIR messaging paper, the title is needed.
- "Zeus-style" DC-net: no system of that name found. Closest hits were Herbivore, Dissent, Zamani et al. and BAR (Springer, paywalled). Not catalogued.
- Mixnets on a Tightrope (S&P 2025): already catalogued by PB7 as `2025-meiser-mixnets-tightrope`; my line is a duplicate pointing to it.
- Elixxir / xx network whitepaper and Nym litepaper (`nym.com/nym_litepaper.pdf`) and the Nym cryptoeconomics paper
  (`nym.com/nym-cryptoecon-paper.pdf`): links seen but not fetched.

## Duplicate and overlap notes for the lead

- Three lines have `status: duplicate` with the other slice's slug: stop-and-go mixnets (H-iog), Hagen et al. contact-discovery abuse (PB6), Mixnets on a Tightrope (PB7). My copies of the two PDFs I had already downloaded were deleted.
- Several PDFs carry the same slug in my catalog and in another collector's (the files already existed when I fetched): PerfOMR, HomeRun, Private Signaling, Scalable Private Signaling, AnNotify (`2017-piotrowska-annotify`), Divide and Funnel, Formal Security Definition of Metadata-Private Messaging. For AnNotify, Divide and Funnel and the formal definition I adopted the other copy's slug. Other PB slices (PB3 receiver privacy, PB7 limits, PB8 post-quantum) will probably also list OMR, PQ Sphinx/Outfox, the trilemma papers and SoKs; the builder keys are title, DOI and arXiv id.

## Seeds for other slices

- PB3 (receiver privacy): UnifOMR (ePrint 2026/910), InstantOMR (2025/2317), SophOMR (2024/1814), Group OMR (2023/534), Snake-eye resistant PKE (2024/510), Private Signaling against active servers (2025/1056), Oblivious Signaling (2026/1975), Lattice multi-recipient KEM (2025/1655), WhisPIR (2024/266), FrodoPIR (PoPETs 2023).
- PB7/PB8 (limits, PQ): "When Mixnets Fail: Evaluating, Quantifying, and Mitigating the Impact of Mixnet Failures" (NDSS 2026, DOI 10.14722/ndss.2026.242384), OptiMix is also NDSS 2026 (10.14722/ndss.2026.232680; ePrint copy is in this catalog), Shift Your Shape (Oldenburg et al., TDSC 2025), Traffic Analysis by Adversaries with Partial Visibility (ESORICS 2023; PDF `esat.kuleuven.be/cosic/publications/article-3637.pdf`), Reward Sharing for Mixnets (J. Cryptoeconomic Systems 2022), Optimizing Anonymity and Performance in a Mix Network (FPS 2021), Compact and Divisible E-Cash with Threshold Issuance (PoPETs 2023), Coconut (NDSS 2019), Onion Routing with Replies (ePrint 2021/1178), Cryptographic Shallots, Divide-and-funnel follow-ups, Rangzen (arXiv 1612.03371), Shared-Dining (arXiv 2104.03032), aDTN (arXiv 1507.08475), TrustMix (arXiv 2606.20251).
- PB6 (deployed messengers): "Practical Attacks on Session Messenger and Oxen Blockchain" (ePrint 2026/773), Signal Private Group System (ePrint 2019/1416), Hashimoto et al., "How to Hide MetaData in MLS-Like Secure Group Messaging" (ePrint 2022/1533).
- H-iog / pub-sub: AnNotify and Verbeth are the two closest items to publish/subscribe in this slice; Pepper, ZIPNet, Spectrum and Express are the DC-net/broadcast line that private pub/sub designs would reuse.

## Reading guide: what the cost models say

- DC-net family: anonymity set bounded by round size; Dissent 5,000 members at best; Riposte 2.9 million users but 32 hours; Spectrum 10,000-user set for a 1 GB file; Blinder 1 million clients in under 8 minutes on GPU; two- or three-server trust.
- Mixnet family: Vuvuzela 1M users at 37 s (12 KB/s per client); Karaoke 2M users at 6.8 s; XRD 2M users at 228 s with cryptographic privacy; Atom 1M tweets in 28 min on 1,024 servers; Alpenhorn 10M users, 150 s dial rounds, 3.7 KB/s. Loopix-style systems (Nym, Katzenpost) have no rounds; their cost is cover traffic and the delay parameter, quantified in the Nym measurement papers (MixMatch, LARMix, LAMP).
- PIR family: Pung 32K users, 4 to 36 MB per message; Talek 32K users, 148 MB per day per client at 1.7 s; Addra 32K users, 726 ms p99; Groove 1M users, 32 s, 100 MB per month; Myco reports 302x to 2,219x higher throughput than PIR baselines by dropping PIR.
- Trusted hardware: TEEMS (220 clients in under 1 s on 205 cores), ZIPNet (TEE only for DoS prevention), PingPong, SGX-Tor, Signal's SGX contact discovery (access-pattern leaks, ORAM not a fit).
- Limits: the anonymity trilemma papers and Kuhn et al.'s SoK explain why flooding (Bitmessage) pays in bandwidth and mixnets pay in latency.
