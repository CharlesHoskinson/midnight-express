# PB8-pq-anonymity: post-quantum and long-term confidentiality for a Bitmessage successor

Catalog: `catalog/PB8-pq-anonymity.jsonl` (89 lines): 64 downloaded, 1 metadata_only, 24 duplicate lines
pointing at records another slice already holds, 0 not_found. Six of the downloaded items are Markdown
captures of web specifications (Tor proposals 263, 269, 340; X-Wing Internet-Draft; RFC 9794; RFC 10024).
`cited_by` is null throughout because OpenAlex refused every request (see Blockers).

## Queries run

- arXiv API (phrase searches): post-quantum + mixnet / onion / Tor; key privacy + ML-KEM; anonymity + Kyber + KEM;
  hybrid + KEM combiner; post-quantum + PIR; post-quantum + anonymous credentials; lattice + group signature;
  record now decrypt later; Grover + proof of work; Grover + SHA preimage; quantum + hashcash;
  post-quantum + metadata + messaging; post-quantum + anonymous + key exchange + Tor. Most returned few or no
  relevant entries, so the ePrint archive was the main index.
- Web search (about 25 queries): Katzenpost hybrid Sphinx; Tor ntor replacement and proposals 263/269/340; ANO-CCA of
  Kyber/ML-KEM; Outfox/Echomix; post-quantum OMR (PerfOMR, Group OMR); lattice anonymous credentials and Privacy Pass;
  Grover and Bitcoin proof-of-work; post-quantum stealth addresses; NIST IR 8545 / FIPS 206 / IR 8547;
  X25519MLKEM768 and RFC 9794; Signal PQXDH and SPQR; Kemeleon/obfuscated KEMs; LeanSig; blind signatures;
  memory-hard functions under quantum adversaries.
- Crossref (4 queries) for "post-quantum mix network packet format", "post-quantum onion routing",
  "quantum Grover proof of work spam hashcash"; found the PoPETs Sphinx proof and a few lattice-PoW leads.
- Direct ePrint metadata pages (citation_* meta tags) for about 70 IDs to confirm titles, authors and years.
  All author lists in the catalog were checked against the first pages of the downloaded PDFs
  (exceptions: BEAR/LION is a scanned PDF; NIST FIPS titles differ in wording only).

## Blockers

- OpenAlex: HTTP 429 on every call from this slice, all session. Not used.
- ePrint PDF endpoint: frequent 429 (shared with other agents); handled with retries and 20-90 s back-offs.
- arXiv API: intermittent 429; a few id_list lookups failed.
- Web search budget was exhausted before the Katzenpost specification HTML pages could be located
  (`katzenpost.network/docs/specs/sphinx.html` returns 404 to the helper). The KEM Sphinx and Sphinx
  specifications were captured by another slice (`spec-katzenpost-kemsphinx`, `spec-katzenpost-sphinx`).
- Springer (PQCrypto 2024) hides "Revisiting Anonymity in Post-quantum Public Key Encryption"; no ePrint copy
  found, so it is metadata_only.

## Sizes that matter for flooding (all verified in the downloaded sources unless marked derived)

| Primitive | Public key | Ciphertext / signature | Source |
|---|---|---|---|
| X25519 | 32 | 32 | Outfox Table 6 |
| ML-KEM-512 / 768 / 1024 | 800 / 1184 / 1568 | 768 / 1088 / 1568 (secret key 1632 / 2400 / 3168) | FIPS 203 |
| X-Wing (ML-KEM-768 + X25519) | 1216 | 1120 | X-Wing draft, RFC 10024 |
| HQC-1 / 3 / 5 (2025 spec) | 2241 / 4514 / 7237 | 4433 / 8978 / 14421 | HQC spec 2025-08-22 |
| HQC-128 / 192 / 256 (round 4) | 2249 / 4522 / 7245 | 4497 / 9042 / 14485 | NIST IR 8545 |
| BIKE level 1 / 3 / 5 | 1541 / 3083 / 5122 | 1573 / 3115 / 5154 | NIST IR 8545 |
| Classic McEliece mceliece460896f | 524160 | 188 | Outfox |
| ML-DSA-44 / 65 / 87 | 1312 / 1952 / 2592 | sig 2420 / 3309 / 4627 | FIPS 204 |
| Falcon-512 / 1024 | 897 / 1793 | sig 666 / 1280 | Falcon spec v1.2 |
| SLH-DSA-128s / 128f / 192s / 192f / 256s / 256f | 32 / 32 / 48 / 48 / 64 / 64 | sig 7856 / 17088 / 16224 / 35664 / 29792 / 49856 | FIPS 205 |
| Bitmessage ECIES wrapper | | 118 bytes beyond the plaintext (IV 16, curve 2, X-length 2, X 32, Y-length 2, Y 32, MAC 32) | Bitmessage protocol spec; derived sum |
| Bitmessage pubkey object | two 64-byte keys | | Bitmessage protocol spec |

Derived estimates (arithmetic on the table, not from a paper): swapping Bitmessage's ECIES ephemeral key for an
ML-KEM-768 ciphertext adds about 1 KB per object, and swapping an ECDSA signature of roughly 70 bytes for
ML-DSA-44 adds about 2.35 KB, so a signed, encrypted object grows by about 3.4 KB (about 1.6 KB with
Falcon-512 as the signature). X-Wing costs only 32 bytes more than ML-KEM-768 alone. A pubkey object grows from 128 bytes of keys to about 2.5 KB (1184 + 1312). Outfox gives
the per-hop law: packet size adds 2(l+1)p, with p the KEM ciphertext length, so four layers of X-Wing add
about 9 KB. PerfOMR shows that an OMR clue costs about 1 KB per message and a public key of about 132 KB,
original OMR needs a 129 MB detection key; SimplePIR needs 121 MB of client hint per 1 GB database.

## Findings by question

- Recipient privacy: post-quantum OMR (Liu-Tromer line) and fuzzy/lattice stealth addresses are the lattice
  replacements for trial decryption; all rest on ring/module LWE. Key-privacy (ANO-CCA) is proven for Kyber
  (Maram-Xagawa, QROM), for most Round-3 KEMs (Xagawa; HQC fails for two of three early parameter sets) and,
  new in 2026, for X-Wing (Bao-Pan). FIPS 203 ML-KEM itself differs slightly from Kyber (public-key hashing);
  nobody here proves ANO-CCA for the final standard text directly. SP 800-227 does not mention anonymity.
  Binding gaps in ML-KEM (Cremers et al., Schmieg attacks) matter for a design that tries one ciphertext
  against many keys.
- Source anonymity: Sphinx-style formats need a NIKE for the compact blinded header; CTIDH hybrid is the only
  NIKE route (Stainton), otherwise KEM-per-hop formats (KEM Sphinx, Outfox) pay about 1.1 KB per hop.
  Tor shows the same wall: 505-byte handshake limit versus 1184-byte ML-KEM keys, solved by proposals 269
  and 340 rather than shipped.
- Session and group security: PQXDH, PQ3 and the Triple Ratchet amortise 2272 bytes (ML-KEM-768 key plus
  ciphertext) by running the PQ ratchet sparsely; Katana cuts this to 1416 bytes. MLS metadata hiding
  (Hashimoto-Katsumata-Prest) is post-quantum by design.
- Limits and costs: anonymous credentials and blind signatures are 22-175 KB per token or proof
  (Beullens 22 KB signature; Agrawal about 45 KB; zkDilithium Privacy Pass 85-175 KB; Jeudy under 650 KB),
  so none can be attached to every flooded object; everlasting-privacy tokens (Chairattana-Apirom et al.)
  are the only design aimed explicitly at record-now-decrypt-later for tokens.
- Proof of work under quantum speedups: Aggarwal et al. estimate an effective 13.8 GH/s from 4.4 million physical
  qubits, over 1000 times slower than a 14 TH/s ASIC; Park-Spooner show the real risk is superlinear
  speedup distorting incentives, not Grover raw speed. Lattice-based PoW (Behnia et al.) and memory-hard
  lower bounds under quantum computation (Beame-Kornerup) are the replacement lines. At the Bitmessage
  minimum difficulty (1000 trials per byte, derived order of 10^6 double-SHA-512 evaluations for a 1 KB
  object before TTL scaling) Grover is irrelevant next to classical GPUs.
- Exposure of recorded Bitmessage traffic: addresses are secp256k1 keys; Google Quantum AI (Babbush et al., 2026)
  and Gidney (2025: under one million noisy qubits for RSA-2048) set the timeline; Mosca's inequality
  frames why a public, permanently replicated object set is the worst case for record-now-decrypt-later.

## Duplicates (24 lines) and shared records

Duplicate lines name the slug held by another slice. Several PB3 lines mark PB8 as canonical, so this
catalog holds the full records for: `2023-pu-fuzzystealthsigs`, `2023-liu-gomr`, `2024-liu-snakeeye`,
`2022-davidson-frodopir`, `2023-li-hintlesspir`, `2001-bellare-keyprivacy`, `2022-grubbs-anonrobustpq`,
`2025-mikic-pqstealth`, `2022-xagawa-anonymitykems`. My own redundant PDF copies were deleted where the
other slice had an identical file (identical sha256). `2018-bindel-hybrid-kem-ake` is kept here because the
other slice's record had no PDF.

## Wanted but not obtained

- FIPS 206 (FN-DSA): not yet published as a draft on csrc.nist.gov at the time of the search; the Falcon spec
  (v1.2) stands in.
- HQC draft standard: none yet; the team specification (2025-08-22) and IR 8545 are used.
- "Revisiting Anonymity in Post-quantum Public Key Encryption" (Cheng, Lu, Li, Li; PQCrypto 2024): paywalled.
- Kemeleon (Elligator-like obfuscation for ML-KEM): only a NIST workshop paper/slides were found; its
  results enter the catalog via the Hybrid Obfuscated KEX and Obfuscated KEX papers.
- Katzenpost Echomix/PQ Sphinx byte tables: the specification pages were not reachable here; no concrete
  header lengths beyond the Outfox formula and the unverified search-snippet example (HeaderLength 476 for
  5 hops, not recorded in the catalog).
- Global Risk Institute Quantum Threat Timeline Report: landing page only, no stable PDF link found.
- OpenAlex citation counts.

## Seeds for other slices

- Lattice or isogeny NIKEs usable in Sphinx (CTIDH, CSIDH, lattice NIKE proposals) and any security audit of
  Katzenpost's KEM Sphinx implementation.
- Signal's SPQR / ML-KEM Braid specification documents (signal.org/docs) and the Katana/hint-MLWE follow-ups.
- Kemeleon and the pq-obfs line (Lyrebird integration) for transport-level hiding.
- "Breaking and (Partially) Fixing Provably Secure Onion Routing" is already in the corpus as `2020-kuhn-breaking`;
  its post-quantum relevance is indirect.
- Tor proposals 249 and 339 (cell widening, UDP-over-Tor) for the cell-size story.
- Anonymous-credential-based rate limiting in deployed pub/sub (Waku RLN) has no post-quantum counterpart
  yet; a search for lattice RLN or post-quantum nullifier schemes is worth one more pass.
