# PB7-limits-theory-soks: collection notes

Slice scope: theory, bounds and systematisations for post-Bitmessage anonymous / metadata-private messaging.
Catalog: `catalog/PB7-limits-theory-soks.jsonl` (72 lines).
Counts: 36 `downloaded` (my own new PDFs), 35 `duplicate` (PDF already held by another slice, `duplicate_of` gives the slug), 1 `metadata_only` (IEEE S&P 2025, no open copy), 0 `not_found`.
Background (pre-2012) items: 3 (Camenisch-Lysyanskaya 2005, Ishai et al. 2006, Pfitzmann-Hansen v0.34 2010).
Every record has the exact statement of its bound or definition in the `note` field (including for `duplicate` lines, so the lead can merge them).

## Bound digest (exact statements are in the catalog notes)

Anonymity trilemma family (global passive adversary, rounds, N users, K nodes, c compromised, l latency, beta/B bandwidth, strong anonymity = advantage negligible):
- Das et al. S&P 2018: impossible if 2*l*beta < 1 - eps(eta), eps = 1/eta^d (synchronised users, l < N, beta*N >= 1). With c >= l compromised nodes: also impossible for l in O(1). With c < l: 2*(l-c)*beta < 1 - eps. Unsynchronised users with send probability p: 2*l*p < 1 - eps.
- Das et al. PoPETs 2020 (user coordination / DC-net shares): unless B >= N-1 (every other user sends a share per real message) the basic condition still applies: p*l < 1 - eps; unified condition l*(p0+beta) < 1 - eps; constant fraction compromised: need l^2 > c (latency superlogarithmic); Anytrust (all but a constant number of nodes compromised): need l^2 > K - gamma.
- Kuhn et al. WPES 2020 SoK: four bounds (Dropping, Trilemma, Counting, Optimality) put on one hierarchy; all prove less than their authors state; Counting = Optimality.
- Gelernter-Herzberg 2013 (Counting-Bound): delivered messages <= messages of the least active honest sender; total sends >= delivered * number of honest senders.
- Ando-Lysyanskaya-Upfal 2018/2021: polylog(lambda) rounds and polylog onions per party per round suffice (O(log^2) rounds, O(log^4) onions in the 2018 paper); for weakly robust + anonymous onion routing against a constant-fraction active adversary dropping f = O(log lambda) onions, onion cost is omega(f(lambda)).
- Jakobsen-Orlandi 2016: no anonymous steganography with key length O(log lambda); a super-logarithmic anonymous seed is required to bootstrap a large anonymous channel.
- Guerraoui et al. (gossip source anonymity, eps-DP against f curious nodes): eps >= ln(f-1) for every gossip protocol on every connected graph; if vertex connectivity <= f no finite eps against a worst-case adversary.
- Dandelion++ (Fanti et al. 2018): D_OPT <= 8 D_FS + 6p^2 + O(p^3) on random 4-regular graphs; p^2 is a lower bound for any estimator.
- DP accounting: Vuvuzela Thm 1 (Laplace noise, eps = 4/b, delta = exp((2-mu)/b)); Stadium Thm 8.1 (Poisson noise); Karaoke optimistic indistinguishability; Meiser-Mohammadi privacy buckets give almost tight upper and lower bounds for r-fold (eps, delta).
- PIR limits: Sun-Jafar capacity C = (1 + 1/N + ... + 1/N^{K-1})^{-1}; Persiano-Yeo t*r = Omega(n log n) (r = Omega(log n)); Corrigan-Gibbs-Kogan C*T >= Omega-tilde(n); Hoover-Persiano-Yeo: with s client bits and k = Omega(s) queries, Omega(n/s) amortised online communication or server cryptographic operations.
- Roos-Strufe 2015: in churn, virtual-overlay maintenance or routing exceeds polylog cost.

## Queries run

Sources that worked: arXiv API (slow, shared 3.5 s gap with many agents, intermittent 429/503), IACR ePrint search page (HTML) and PDFs, AnonBib cache (freehaven.net/anonbib, listing of ~487 cached PDFs scanned by file name), Crossref (DOI and cited-by metadata), author pages (mohammadi.eu, robgjansen.com), PoPETs and USENIX open PDFs.

- WebSearch (about 20 calls, then the session budget of 200 was exhausted by other agents): trilemma, comprehensive trilemma, privacy notions, AnoA, TUC, UC onion routing, ALU18/ALU21, Gelernter-Herzberg, Oya dummies, Kuhn breaking, Sphinx proofs.
- arXiv (query files q2, q3, q4, about 40 queries): anonymity trilemma; anonymous communication lower bound/impossibility; metadata-private messaging; SoK anonymous communication; onion routing UC; Dandelion; rumor source obfuscation; differential privacy + mix/private messaging; DC-net / dining cryptographers; anonymous broadcast; survey anonymous communication; privacy-preserving measurement Tor; PIR lower bound; Nym; sealed sender; statistical disclosure; anonymity + gossip; decentralized messaging; Bitmessage (zero hits on arXiv); oblivious message retrieval; cover traffic; unlinkability definition.
- ePrint search (about 20): anonymous communication lower bound; anonymity trilemma; mix network DP; UC onion; DC-net anonymous broadcast; private messaging definition; SoK anonymous communication; PIR lower bound; mixnet leakage; sealed sender; anonymous channel impossibility; repliable onion; Untagging Tor; OMR lower bound; unlinkability definition.
- Crossref bibliographic lookups for all kept titles (DOIs, cited-by).
- AnonBib cache file-name scan: identified Camenisch-Lysyanskaya, Ishai et al., TASP, Rochet-Pereira, Roos et al., I2P and Freenet measurement.
- OpenAlex: not usable (429 on every call, whole session). Semantic Scholar: 429.

## Hosts that blocked or throttled

- api.openalex.org: 429 throughout; Semantic Scholar graph API: 429.
- eprint.iacr.org PDFs: frequent 429 (shared IP, many agents); retries with 30 s back-off eventually worked for most; Gelernter-Herzberg and Untagging Tor needed several rounds.
- export.arxiv.org: 429 and 503 on bursts; some queries in q3/q4 gave no result.
- publications.cispa.saarland: JavaScript app, no direct PDF link; used the author page instead.
- WebSearch: session budget exhausted.

## Wanted but not obtained

- Mixnets on a Tightrope (Meiser, Das, Kirschte, Mohammadi, Kate; IEEE S&P 2025, doi 10.1109/SP61157.2025.00233): no open copy found; catalogued `metadata_only`. The bound statement (provably optimal heuristic adversary) is therefore not read.
- Hevia and Micciancio, "An indistinguishability-based characterization of anonymous channels" (PETS 2008, the "Optimality-Bound"): no open PDF located (background item, not catalogued).
- Pre-2012 background not collected (cap 25 for the wave): Chaum 1981 and 1988, Serjantov-Danezis, Diaz et al. "Towards measuring anonymity", Troncoso-Danezis Bayesian traffic analysis, Klonowski-Kutylowski mix provable anonymity, Mathewson-Dingledine statistical disclosure. I took only three.
- Measurement of anonymity-set size and user behaviour for messengers, Nym, Matrix, Nostr and Bitmessage itself: no usable study found in this slice's sources (Bitmessage has no arXiv hits). Tor measurement is covered by Jansen-Johnson (PrivCount), Mani et al., Johnson et al., Biryukov et al. HisTorE (Fenske et al., PETS 2017), PrivEx (Elahi et al. CCS 2014) were not located.
- A SoK or survey specific to decentralized (non-Tor) messaging: none found. Closest are Sasy-Goldberg (31 systems), Shirazi et al. (routing taxonomy), Shirali et al. (DC-nets), Infeld-Stainton (mixnet review) and Unger et al. (secure messaging).
- Cryptographic Shallots, Untagging Tor, Onion Routing with Replies are kept as building blocks; Degabriele-Stam and Ando-Lysyanskaya were found late via ePrint search.

## Housekeeping

- Several other slices fetched the same papers under different slugs at the same time. I deleted my own byte-identical or alternate-version copies and recorded the paper as `duplicate`: 2018-das-anonymity-trilemma, 2017-sun-capacity-pir, 2021-ando-complexity-anonymous-communication, 2020-kuhn-breaking-provably-secure-onion, 2020-das-comprehensive-trilemma, 2020-kuhn-sok-performance-bounds, 2013-biryukov-trawling-tor, 2013-johnson-users-get-routed, 2015-unger-sok-secure-messaging, 2019-kuhn-privacy-notions, 2018-hoang-i2p-empirical.
- Zhang et al. (2022/1139), AnNotify and Divide-and-Funnel were downloaded by me and by PB2 under the same slug; the file is shared, my catalog line is marked `duplicate` with the same slug.
- I also deleted PDFs of six papers I fetched and judged off-scope: Cherubin "Bayes, not Naive" (website-fingerprinting bounds), Khattak et al. "Do you see what I see", Li et al. WF leakage, Thomas-Mohaisen onion DNS leakage, Tippe-Tippe onion services in the wild, Geddes et al. "How low can you go". A wrong arXiv id (1706.05196) was downloaded once and removed; the correct Shirazi survey is arXiv 1608.05538.
- Years: where the arXiv posting is later than the venue (Oya et al. 2013/2014 posted 2019) the record year is the venue year; slug prefixes follow that year.
- Venue of Guerraoui et al. (arXiv 2308.02477, v2 Dec 2025) and of Divide-and-Funnel (ePrint 2021/1685) not verified.

## Seeds for other slices

- Schadt, Coijanovic, Strufe, "Breaking and (Partially) Fixing Onion Routing with Fragmentation", PoPETs 2026, doi 10.56553/popets-2026-0120 (follow-up to Kuhn et al.; surfaced by Crossref).
- Rahimi, "When Mixnets Fail: Evaluating, Quantifying, and Mitigating the Impact of Adversarial Nodes", NDSS 2026, doi 10.14722/ndss.2026.242384.
- Cinal et al., "Beyond Anonymity Sets: A Security Model for Distributed Shuffling in Adversarial Environments", ePrint 2026/1258 (security model for shuffling; not read).
- Kuhn, "Plausible Deniability for Anonymous Communication" (WPES 2021, doi 10.1145/3463676.3485605) seen in search results, not fetched.
- Degabriele-Stam and Kuhn et al. hierarchies suggest chasing "Onion Encryption Revisited" (relations among security notions, 2025) and Scherer-Weis-Strufe Sphinx proofs (already held by another slice).
- Brigham-Hopper (sealed-sender groups) and Martiny et al. (Improving Signal's Sealed Sender) are held by another slice; they are the closest published measurements of user-behaviour leakage in a deployed messenger.
