# Review: "Bitmessage: A Comprehensive Technical Guide to Its Protocol, Privacy, Security, Implementations, and Future"

## Verdict

A sound, careful protocol analysis whose facts survive checking. Its weakness is not accuracy but
coverage and finish: it analyses Bitmessage in isolation, cites almost no academic literature, and
ships with citation placeholders instead of references.

## Checked and correct

| Claim | Check |
|---|---|
| PyBitmessage is not archived, default branch `v0.6`, last push 29 May 2026 | GitHub API: `archived: false`, `pushed_at 2026-05-29T16:17:56Z` |
| Pinned head `dcbcc4a2…`, 29 May 2026, signed | GitHub API: sha matches, committed 2026-05-29T16:09:27Z, `verified: true` |
| Release line stops in February 2018 | Releases are v0.6.3 and 0.6.3.2 (13 Feb 2018), v0.6.2 (1 Mar 2017), v0.6.1, v0.6.0 |
| 0.6.3 shipped as an emergency fix for a 0.6.2 remote-code-execution bug and added Dandelion++ | Release text says both |
| `setup.py` is still Python 2.7 | Shebang `#!/usr/bin/env python2.7` and classifier `Python :: 2.7 :: Only` at the pinned commit |
| Dandelion constants: two stems, 600 s reassignment | `src/network/dandelion.py`: `MAX_STEMS = 2`, `REASSIGN_INTERVAL = 600`, exponential fluff delay plus 10 s fixed |
| Worked address `BM-BcbRqcFFSQUUmXFKsPJgVQPSiFA3Xash` | Base58 decodes to `02 01 df24…1d3d4 ca229190`; double-SHA-512 checksum matches |
| Proof-of-work example: 4,636,718.75 denominator, T ≈ 3.978×10¹², p ≈ 2.157×10⁻⁷ | Recomputed exactly |
| Bandwidth scenario table (28 MiB, 281 MiB, 2.75 GiB per day; 0.77, 7.69, 76.9 GiB per 28 days) | Recomputed exactly |

The cryptographic description (ECIES-like secp256k1 ECDH, SHA-512 key split, AES-256-CBC,
HMAC-SHA-256, no forward secrecy) and the framing constants match the protocol documentation as I
know it. The central reasoning is right and well stated: an ephemeral sender key does not give
forward secrecy when the recipient key is static; an acknowledgement is not a read receipt; a chan
is a shared identity, not a group.

## Weaknesses

1. **No resolvable references.** The text carries tool markers (`citeturn…`, `fileciteturn…`) on
   nearly every paragraph and the annotated bibliography lists titles without URLs, DOIs or
   versions. A reader cannot follow a single citation. These markers must become real footnotes
   before the document is shared.
2. **The academic literature is missing.** The only peer-reviewed source is the 2015 secure
   messaging SoK. Nothing on Dandelion (Venkatakrishnan et al., 2017) or Dandelion++ (Fanti et al.,
   2018) and its anonymity analysis, although the report leans on both. Nothing on the metadata-private
   messaging line (Dissent, Riffle, Vuvuzela, Alpenhorn, Pung, Stadium, Karaoke, Loopix, XRD, Addra),
   nothing on fuzzy message detection or oblivious message retrieval, which formalise the same
   "download everything and trial-decrypt" idea that Bitmessage uses, and nothing on the anonymity
   trilemma, which bounds the flooding trade-off the report discusses informally.
3. **The direct descendants are absent.** Ethereum Whisper and Waku (topic Bloom filters plus
   proof-of-work), Swarm PSS, Nostr direct messages, Zcash-style note scanning and Bitchat are
   closer relatives than Signal or Matrix, yet the comparison table skips them.
4. **The comparison table mixes layers.** Signal, MLS and OpenPGP are session or content protocols;
   Bitmessage, Briar and SimpleX are transport and delivery designs. Rows should be grouped by
   which problem each one solves (delivery, source anonymity, session security, group
   membership) so that "Bitmessage lacks X" is not asked of systems that never aimed at X.
5. **Anti-spam is asserted, not argued.** The proof-of-work section gives the formula but no
   economics: no use of the Laurie–Clayton critique of proof-of-work for spam, nothing on
   rate-limiting nullifiers or anonymous credentials as alternatives.
6. **The evidence boundary is avoidable.** The report states that no live census was done. A crawl
   of the public network from the bootstrap nodes would have given node count, stream occupancy and
   object rates, which is the data that decides whether the anonymity-set argument is large or small.
7. **Dandelion is described qualitatively.** The adversary model of Dandelion++ (honest-but-curious
   spies holding a fraction of nodes) is not stated, so the privacy gain is not bounded.
8. **Smaller points.** The scalability model omits `inv` and `getdata` overhead (acknowledged but
   not estimated). The Session row describes a roadmap rather than the shipped protocol. The
   timeline cites "Nov. 16, 2014" for protocol v3 without distinguishing the announcement from
   enforcement.

## Recommended repair

Resolve every marker into a footnote with title, author, date and URL or DOI. Add a related-work
section covering items 2 and 3. Regroup the comparison by problem solved. Add a short anti-spam
section with the economic argument. If a measurement is wanted, crawl the bootstrap peers and report
object rates by stream.
