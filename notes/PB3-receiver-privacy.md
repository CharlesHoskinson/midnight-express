# PB3-receiver-privacy: collection notes

Slice: cryptographic building blocks that let a recipient fetch or detect its messages without every
node downloading and trial-decrypting everything (fuzzy message detection, oblivious message retrieval,
private signaling, PIR and keyword PIR, key-private encryption, stealth addresses and view tags,
Bloom-filter and compact-filter subscriptions, PSI and private contact discovery, wallet note-scanning
specifications). Collected 2026-10-01.

## Result

`catalog/PB3-receiver-privacy.jsonl` holds 120 lines (state at the final build):

| status | count |
|---|---|
| downloaded (unique to this slice at build time) | 74 |
| duplicate (already in another cluster, existing slug named) | 46 |
| metadata_only | 0 |
| not_found | 0 |

The 46 duplicate lines carry this slice's receiver-privacy note and Bitmessage link; the existing slug
is in `slug` and my own slug in `my_slug`. They sit in PB2 (24), PB8 (9), PB1 (5), PB6 (5), PB7 (3).
Several PB slices were writing at the same time, so more overlaps may appear once their catalogs
are final; the lead should rerun a title/DOI/ePrint-id dedupe. Of the 74 unique records, 21 are `core`,
53 `adjacent`, 3 are `background` (Chor et al. PIR 1998, Boneh et al. PEKS 2004, Ostrovsky-Skeith
private streaming search 2005). Bellare et al. key-privacy (2001) is a fourth background item, but PB8 already catalogued it.

Roles among the unique records: building_block 41, system 16, limit_or_theory 7, attack_or_audit 4,
measurement 3, sok_or_survey 3.

Specs saved as Markdown page text (not PDF): Penumbra FMD (six pages concatenated), ZIP 307, BIP 47,
BIP 37, BIP 157, BIP 158, ERC-6538, Monero research-lab issue 73, Monero PR 8061 (plus BIP 352, ERC-5564,
EIP-627, which another slice holds). The Zcash protocol specification is the PDF
(v2026.7.0-236 NU6.2, dated 2026-09-30, 236 pages). The saved GitHub pages include site navigation text above the real content.

## Cost numbers collected (server work, bandwidth, latency)

Recipient-side detection and outsourcing:

- FMD (Beck et al., CCS 2021): p = 2^-n up to n = 24, 68-byte flag, 1.927 ms create, 0.548 ms test at p = 3%;
  fractional-p scheme 0.3-1.2 MB ciphertext, 18.1 ms create, 9.6 ms test. Privacy is the false-positive
  rate: lower p means less download and a smaller anonymity set. Seres et al. and Frank et al. show
  the rate must be tuned to the traffic graph and that selfish users make FMD unviable without altruists.
- Private signaling (Madathil et al., USENIX Sec 2022): TEE server 116-157 ms per signal, two-server
  garbled circuits minutes per signal. Scalable Private Signaling (TEE+ORAM): under 70 ms per sent message,
  under 6 s per retrieval of 100 signals at 1M recipients and 10M messages. Actively secure two-server
  version: 33.57 KB digest at 2^19 messages, about 2 min retrieval on 16 threads.
- OMR (Liu-Tromer, CRYPTO 2022): about $1 per million messages scanned, digest decoded in under 20 ms,
  about 0.1 s per message server time and 132 KB public key for the baseline. GOMR: about $3.36 per
  million messages with up to 15 recipients each. PerfOMR (USENIX Sec 2024): about 40 ms per message,
  key 235x smaller. HomeRun: 3830x less server time than FHE OMR with two non-colluding servers.
  SophOMR: 3.4x faster than PerfOMR on 65,536 payloads of 612 bytes. InstantOMR: about 860x lower latency than
  SophOMR. UnifOMR: 2^19 messages of 612 bytes in about 25 s with 4 MB communication (SophOMR: over 1250 s,
  260 KB); also proves OMR with strong detection-key-unlinkability is at least as hard as PIR, which is the
  cost floor for any non-broadcast recipient-hiding scheme. FPGA matrix-vector step: 13.86x over software.
- Kerblam (OMR + oblivious shuffle, two servers): 5.577 s per message at 2^20 messages of 1 KB.

PIR for message boards:

- SealPIR: queries 274x smaller than XPIR for 11-24% more server CPU. OnionPIR: 4.2x response overhead.
  Spiral: 1.9 GB/s, rate 0.81. SimplePIR: 10 GB/s/core, 121 MB hint per 1 GB database, 242 KB per query;
  DoublePIR 16 MB hint, 345 KB/query. YPIR: 12.1 GB/s/core and 2.5 MB total on 32 GB with no hint.
  Respire: 6.1 KB online for a 256-byte record out of over a million. FrodoPIR: under 1 s per query on
  1M x 1 KB, about $1 per 100,000 queries. Piano (PRFs only): 73 ms on a 100 GB database at 60 ms RTT.
  Checklist: 3.3x communication and 9.8x server compute over the non-private lookup.
- Message systems built on PIR or DPF: Pung up to 1.3 s per message at 1M tuples; Addra 32K clients, 726 ms
  p99, PIR cost quadratic in users; Talek 9,433 messages/s for 32,000 users at 1.7 s; Myco O(N log^2 N) and up to
  2,219x over single-server PIR systems; Express over 100x less bandwidth than Pung and Riposte; Alpenhorn 10M
  users, 150 s dial latency, 3.7 KB/s per client; 2PPS (pub/sub) 100,000 clients at 5 s end to end; DP5 about
  $0.50 per user per month at 1M users.
- Keyword PIR (lookup by tag): ChalametPIR within 1.08x of index PIR; KPIR 47 ms for 1M x 32-byte entries; LetoPIR
  12.4-17x less communication than SparsePIR.
- Limits: Chor et al. (one server must send the whole database for perfect privacy); Sun-Jafar PIR capacity
  1 + 1/N + ... + 1/N^(K-1); Persiano-Yeo t*r = Omega(n log n) for preprocessing PIR.

Chains and wallets:

- Zcash Sapling (ZIP 307): 580-byte ciphertext + 32-byte ephemeral key per output; compact form 116 bytes per output
  (80% saved) and 32 bytes per spend (90% saved); the client still trial-decrypts every output.
- Silent Payments (BIP 352): one ECDH per eligible transaction; light client 33 bytes of tweak data per eligible
  transaction, about 30 MB/month scanning every 3 days, 30-50 MB/month every block, 450 MB/month worst case; sender-chosen
  data can inflate scan cost (K_max = 2323 cap; Qian et al. Omega(N+KM) bound).
- 1-byte view tags: Monero 30-40% faster scanning, about 99.6% of outputs skip the EC step (the proposer estimated 50-70%);
  ERC-5564 reduces non-matching announcements to one multiplication plus one hash.
- Bloom filters (BIP 37 / Whisper): a client with under 20 addresses leaks almost all of them (Gervais et al.); BIP 157/158
  client-side filters leak nothing to the server but cost a filter per block (Kotzer-Rottenstreich measure the trade-off).
- Contact discovery: PIR-PSI 1.36 s and 4.28 MiB for 1,024 contacts vs 67M users; Hetz et al. under 2 s for 1,024 contacts
  vs over 2 billion users; Chen et al. FHE-PSI 12.5 MB for 5,000 vs 16M items.

## Findings that matter for the review

1. Every non-broadcast scheme needs the recipient to hold a handle (tag, label, slot, identity, detection key). Bitmessage's
   design avoids that by flooding; FMD, OMR and private signaling keep the flood but outsource the scan; PIR, Pung, Talek, Express
   and PIB3 replace the flood with addressed retrieval and need a shared secret, epoch or identity to compute the slot.
2. UnifOMR's PIR reduction and the PIR lower bounds give a floor: recipient-hiding retrieval costs at least about PIR.
3. FMD gives a tunable anonymity set (the false-positive rate); the analyses (Seres et al., Penumbra's parameter page) show it leaks
   over time and with traffic structure. 1-byte view tags are a hard-coded p = 1/256 version of the same idea.
4. Trusted-hardware shortcuts recur (ZLiTE, Private Signaling, Scalable Private Signaling, TEEMS); the TEE-free options need two
   non-colluding servers (HomeRun, Kerblam, Express, Myco, 2PPS) or FHE (OMR line).
5. Anonymity needs more than IND-CCA: key-privacy and robustness (Bellare 2001; Kohlweiss 2013; Grubbs 2022; Xagawa 2022);
   non-committing AEAD enables multi-key attacks on trial decryption (Len et al.). RFC 9180 (HPKE) was fetched and a text search finds no
   key-privacy or anonymity statement in it, so a Bitmessage successor on HPKE has to cite the KEM analyses directly.
   (RFC 9180 itself is not catalogued: no content on this topic.)
6. Scan-DoS is real on chains where senders choose what recipients process (BIP 352 analysis), mirroring the spam problem that
   Bitmessage addresses with proof-of-work.

## Queries run

- ePrint site search (rate-limited, results sorted by id): oblivious message retrieval; fuzzy message detection; detection key;
  private signaling; stealth address; SimplePIR; Spiral; Respire; FrodoPIR; Piano; Checklist; DoublePIR; OnionPIR; keyword PIR;
  private information retrieval without preprocessing single-server; private contact discovery; anonymous public key encryption key
  privacy; key-private; anonymity robust encryption; publish subscribe encryption; public key encryption with keyword search; private
  set intersection discovery; Bloom filters lightweight bitcoin clients; Clarion; Zcash; Monero; silent payments; private searching on
  streaming data; recipient privacy; receiver anonymity; private notification; oblivious synchronization; light client privacy; wallet
  synchronization; private information retrieval blockchain; bulletin board recipient; payment detection; metadata-private messaging;
  anonymous messaging; fuzzy; oblivious message; detect messages server; tag; TreePIR; SealPIR; Riposte; and a few others that returned nothing
  useful ("Express", "Penumbra", "Sapling shielded wallet scanning" and similar). Each query returned a few to a few hundred hits.
- arXiv API: "fuzzy message detection", "oblivious message retrieval", private information retrieval AND messaging (capacity-style PIR
  papers, out of scope except Sun-Jafar), publish/subscribe AND private information retrieval (2PPS found), note scanning / trial decryption,
  light client AND shielded.
- Crossref: private publish subscribe searchable encryption; privacy-preserving publish/subscribe untrusted broker; PIR publish subscribe.
  Results were paywalled pub/sub confidentiality papers (see "wanted").
- HAL API: XPIR (found), Thrifty privacy (not in HAL).
- Web searches (before the session budget of 200 ran out) for Penumbra FMD, ZIP 307, BIP 352, ERC-5564, Pung, Express, Zcash protocol spec,
  CryptoNote, Zero to Monero, Monero view tags, Riposte, key-privacy, DP5, Alpenhorn, Whisper/Waku, Chor et al. PIR, PingPong.

## Hosts that blocked or limited

- OpenAlex answered 429 on every attempt during this run (about a dozen tries over an hour), so OpenAlex was not used for discovery or `cited_by`;
  all `cited_by` are null.
- eprint.iacr.org answered 429 many times under load from the parallel agents (the shared per-host lock queued fetches for 2-6 minutes each).
  Backoff of 30-60 s with up to 6 retries; every wanted ePrint PDF was eventually obtained. The ePrint search page returned 404 for some
  multi-word queries and then worked for the same query later (transient).
- WebSearch hit its session cap (200 calls), so the last searches (Aztec note tagging, private pub/sub with PIR, Zcash light-client
  measurement papers, Waku filter RFC) were not run.
- DBLP and Semantic Scholar were not tried. CORE not tried.

## Wanted but not obtained (no legal open copy found, or not reached)

- Confidentiality-preserving pub/sub papers behind paywalls: Barazzutti et al. "Thrifty privacy" (DEBS 2012), Nabeel et al. (SACMAT 2012),
  Onica et al. "Efficient key updates through subscription re-encryption" (Middleware 2015), Raiciu-Rosenblum (2006, too early).
- Courtois-Mercer "Stealth address and key management techniques in blockchain systems" (ICISSP 2017), the dual-key stealth address reference
  cited by Madathil et al.; Todd's 2014 stealth address proposal; Kushilevitz-Ostrovsky 1997 single-database PIR; Sion-Carbunar 2007 and
  Olumofin-Goldberg 2011 on PIR practicality (all background, not pursued).
- Aztec note tagging / private message delivery documentation; Waku 12/WAKU2-FILTER and 13/WAKU2-STORE RFCs; Signal private contact discovery
  (SGX) blog; Apple's PIR caller-ID lookup (swift-homomorphic-encryption) documentation. These are specs or blog posts that would need a
  fetch; Apple's deployment is only evidenced by the LetoPIR introduction.
- ZIP 314 (privacy upgrades to the Zcash light client protocol) is a reserved stub; no content.
- Plinko, RMS24 (Ren-Wang), Shi et al. CRYPTO 2021 puncturable pseudorandom sets and other preprocessing-PIR variants were left out as
  repetitive after Piano/TreePIR/Checklist/CGHK22.

## Seeds for other slices

- Pub/sub confidentiality line (not receiver privacy): Nabeel/Shang/Bertino, Onica et al., Barazzutti et al., Denis et al. (2020) "Privacy-preserving
  content-based publish/subscribe with encrypted matching and data splitting", Wang et al. PCP (IEEE Access 2017), Gao et al. (2024). Slice A or D.
- Waku filter, store and light-push (light-node subscription) RFCs and the Waku paper (PB slice for Waku/Status).
- Mixnet-with-PIR and OT delivery: AOT, Express, Clarion, Trellis (ePrint 2022/1548), DumboMix (2026/1699), SecureDrop protocol (2026/1484),
  Formal definition of metadata-private messaging (2022/1139), TEEMS (2025/1102), PingPong (arXiv 2504.19566). Most are already in PB2.
- Zcash/Namada/Penumbra side: Namada FMD implementation notes (Heliax), Orchard/ZIP 316 unified-address viewing-key analyses; ZIP 212.
- Private information retrieval with evolving databases (incremental PIR, ePrint 2026/030, 2026/1077) for message boards that change per epoch.
- Duplicate-handling remarks for the lead: PB2 holds the Hetz-Schneider-Weinert contact-discovery PDF under the slug
  `2023-kales-contactdiscoverybillions` (wrong first author in the slug). `pdfs/2022-hagen-contactdiscovery.pdf` is a byte copy of my
  `pdfs/2022-hagen-contactdiscoveryattacks.pdf` (ePrint 2022/875) and was not catalogued by anyone at build time;
  `pdfs/2021-hagen-contactdiscovery.pdf` is a byte copy of `pdfs/2021-hagen-contact-discovery.pdf` (ePrint 2020/1119).
- I removed five byte-identical or text-identical copies of my own downloads where PB slices already held the document under another slug
  (Hetz et al., Frank et al., PIB3, BIP 352 page, ERC-5564 page) and one stray download (random-index PIR, off topic).
