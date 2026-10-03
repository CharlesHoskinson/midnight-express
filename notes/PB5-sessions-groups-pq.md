# PB5-sessions-groups-pq: collection notes

Slice scope: session security and group security that Bitmessage's static-key encryption lacks (Signal family, Apple PQ3, MLS, Matrix, WhatsApp group analyses, key transparency, post-quantum hybrid key exchange and signatures, SoK papers). Run date 2026-10-01.

## Result

- Catalog lines: 171 in `catalog/PB5-sessions-groups-pq.jsonl`.
- downloaded: 142 (PDF or saved Markdown page text under `pdfs/`), metadata_only: 2, not_found: 0, duplicate: 27 (already catalogued by another slice; the line carries the existing slug and this slice's reading in `note` and `bitmessage_link`).
- Roles among the non-duplicate lines: attack_or_audit 24, building_block 48, limit_or_theory 32, sok_or_survey 5, system 35.
- Background (pre-2012 foundations): 3 (2004-borisov-otr, 2009-goldberg-mpotr, 2006-diraimondo-deniable).

## Queries run

IACR ePrint (`eprint.iacr.org/search?q=`, result pages then each record page for title, authors, abstract and venue):

- `title:ratchet`
- `title:"sealed sender"`
- `title:Signal AND title:handshake`
- `title:"continuous group key agreement"`
- `title:MLS`
- `title:"key transparency"`
- `title:"transparency" AND title:messaging`
- `title:"hybrid" AND title:KEM`
- `title:"secure messaging"`
- `title:"group messaging"`
- `title:"multi-device"`
- `title:"post-quantum" AND title:messaging`
- `title:iMessage`
- `title:Matrix AND title:encryption`
- `title:WhatsApp`
- `title:Telegram`
- `title:Threema`
- `title:"post-compromise"`
- `title:"Sesame" OR title:"sender keys"`
- `title:"message franking"`
- `title:SPQR OR title:PQXDH OR title:X3DH`
- `title:"Double Ratchet"`
- `title:"Messaging Layer Security"`
- `title:"sparse continuous key agreement"`
- `title:"Signal" AND title:"post-quantum"`
- `title:"key transparency" AND title:SoK`
- `title:"TextSecure"`
- `title:ratcheting`
- `title:SoK AND title:messaging`
- `title:"group key agreement" AND title:messaging`
- `title:"post-quantum" AND title:"group"`
- `title:"hybrid" AND title:"combiner"`
- `title:"authenticated KEM" OR title:"AKEM"`
- `title:"anonymous" AND title:"group messaging"`
- `title:"Signal" AND title:"group"`
- `title:deniability AND Signal`
- `title:MLS AND title:metadata`

HAL API (`api.archives-ouvertes.fr/search`): TreeKEM; Formal Models and Verified Protocols for Group Messaging; Automated Verification for Secure Messaging Protocols; Formal verification PQXDH; Messaging Layer Security formal; continuous group key agreement; secure group messaging; Signal protocol post-quantum; Double Ratchet; key transparency; End-to-End Encrypted Messaging Protocols overview; Transparency Dictionaries.

arXiv API: `abs:"Messaging Layer Security"`, secure messaging + post-compromise, key transparency, group messaging + end-to-end, Matrix + Megolm (503 from the API), sealed sender, Signal protocol analysis, post-quantum + secure messaging, SoK + secure messaging, group chat + encrypted, WhatsApp + group + attack, Double Ratchet, TreeKEM, SoK/survey variants (a last batch returned only content-moderation SoKs, not collected).

Other: direct probes of signal.org specification and blog pages, security.apple.com, rfc-editor.org, datatracker.ietf.org, nvlpubs.nist.gov, gitlab.matrix.org raw docs, usenix.org, ndss-symposium.org, petsymposium.org, ieee-security.org, cacr.uwaterloo.ca, cypherpunks.ca, whatsapp.com, about.fb.com, wire-docs.wire.com. Two WebSearch queries (Martiny sealed sender; Telegram MTProto paper); the tool's search budget was then exhausted. OpenAlex title lookups for about 50 titles (only 38 answered; used for DOI and `cited_by` where available, null elsewhere).

## Hosts that blocked or throttled

- `eprint.iacr.org`: HTTP 429 on both record pages and PDFs during long stretches (roughly 10:30 to 11:00 and again around 11:15 to 11:40 local time on 2026-10-01, shared load from other collection agents) and one short DNS failure at 11:46. `scripts/pe_fetch.py` retries with 30 to 60 s sleeps; the PDF downloader used a 12 s gap and a 10 minute back-off after three consecutive 429s. Every ePrint PDF was eventually retrieved.
- `api.openalex.org`: frequent 429; DOI and citation counts missing for most records.
- `export.arxiv.org`: slow under shared load, otherwise answered.
- Not used: DBLP, CORE, Semantic Scholar, Unpaywall, Sci-Hub-type mirrors. No email address was sent anywhere.

## Wanted but not retrieved (metadata_only)

- `2016-ermoshina-e2eoverview`: End-to-End Encrypted Messaging Protocols: An Overview (INSCI 2016 (Internet Science), Springer LNCS) https://doi.org/10.1007/978-3-319-45982-0_22
- `2006-diraimondo-deniable`: Deniable Authentication and Key Exchange (ACM CCS 2006 (IACR ePrint 2006/280)) https://eprint.iacr.org/2006/280

## Records marked duplicate (already in another slice)

- `2016-signal-x3dh-spec`: The X3DH Key Agreement Protocol
- `2016-signal-double-ratchet-spec`: The Double Ratchet Algorithm
- `2023-signal-pqxdh-spec`: The PQXDH Key Agreement Protocol
- `2017-signal-sesame-spec`: The Sesame Algorithm: Session Management for Asynchronous Message Encryption
- `2025-signal-mlkem-braid-spec`: The ML-KEM Braid Protocol (Sparse Post-Quantum Ratchet specification)
- `2025-draft-xwing-kem`: X-Wing: general-purpose hybrid post-quantum KEM (draft-connolly-cfrg-xwing-kem-11)
- `2016-matrix-olm-spec`: Olm: A Cryptographic Ratchet
- `2016-matrix-megolm-spec`: Megolm group ratchet
- `2016-whatsapp-security-whitepaper`: WhatsApp Encryption Overview: Technical white paper (Version 9)
- `2021-martiny-sealed-sender`: Improving Signal's Sealed Sender
- `2023-brigham-sealed-sender-groups`: No safety in numbers: traffic analysis of sealed-sender groups in Signal (poster)
- `2022-albrecht-telegram`: Four Attacks and a Proof for Telegram
- `2024-bhargavan-pqxdh`: Formal verification of the PQXDH Post-Quantum key agreement protocol for end-to-end secure messaging
- `2023-paterson-threema`: Three Lessons From Threema: Analysis of a Secure Messenger
- `2016-cohngordon-signal`: A Formal Security Analysis of the Signal Messaging Protocol
- `2018-alwen-double-ratchet`: The Double Ratchet: Security Notions, Proofs, and Modularization for the Signal Protocol
- `2025-dodis-triple-ratchet`: Triple Ratchet: A Bandwidth Efficient Hybrid-Secure Signal Protocol
- `iog-security-analysis-and-improvements-for-the-ietf-mls-standard`: Security Analysis and Improvements for the IETF MLS Standard for Group Messaging
- `iog-modular-design-of-secure-group-messaging-protocols-and-the-s`: Modular Design of Secure Group Messaging Protocols and the Security of MLS
- `iog-continuous-group-key-agreement-with-active-security`: Continuous Group Key Agreement with Active Security
- `2023-albrecht-matrix`: Practically-exploitable Cryptographic Vulnerabilities in Matrix
- `2017-rosler-more-is-less`: More is Less: On the End-to-End Security of Group Chats in Signal, WhatsApp, and Threema
- `2023-malvai-parakeet`: Parakeet: Practical Key Transparency for End-to-End Encrypted Messaging
- `2018-bindel-hybrid-kem-ake`: Hybrid Key Encapsulation Mechanisms and Authenticated Key Exchange
- `2019-chase-signal-private-groups`: The Signal Private Group System and Anonymous Credentials Supporting Efficient Verifiable Encryption
- `2026-esposito-verbeth`: Verbeth: Secure Messaging with Metadata Minimization over Public Blockchain Logs
- `2023-matrix-core-formal`: Device-Oriented Group Messaging: A Formal Cryptographic Analysis of Matrix’ Core

Heads-up for the lead: at the end of the run `pdfs/` held uncatalogued files from other agents that are the same papers as PB5 records (for example `pdfs/2022-hashimoto-hide.pdf` and `pdfs/2021-weidner-key.pdf`, PB5 slugs `2022-hashimoto-mls-metadata` and `2020-weidner-decentralized-sgm`). These may become duplicates when those slices write their catalogs.

Duplicates were detected by title, DOI and arXiv id against the other `catalog/*.jsonl` files at the end of the run. For PB6 and PB1 the existing file under `pdfs/` is the canonical copy.

## Corrections made during the run

- Several URLs were guessed and then checked against the file content before cataloguing; one PoPETs 2018 URL (popets-2018-0011) turned out to be an unrelated Tor paper, and the correct Unger and Goldberg paper is popets-2018-0003.
- Author lists for arXiv preprints 2305.09799 (Brigham and Hopper), 2607.27510 and 2410.06587 were taken from the PDF first page, not from the search snippet.
- While deduplicating, one cleanup step briefly removed two PDFs (`pdfs/2023-paterson-threema.pdf`, `pdfs/2022-albrecht-telegram.pdf`) that another slice's catalog also points to under the same slug; both were re-downloaded from the same URLs and match the sha256 recorded in that catalog.

## Scope notes

- Source types: IETF RFCs and drafts (MLS, HPKE, hybrid TLS, key transparency, X-Wing), NIST FIPS 203, 204, 205 and SP 800-227, Signal and Matrix specifications, Apple, WhatsApp, Messenger and Wire technical documents, and academic papers. Web pages were saved as Markdown (`pdfs/*.md`) only when no PDF exists; email addresses inside saved IETF text were replaced by a placeholder.
- `year` is the earliest public version year. For IETF drafts and vendor whitepapers whose first revision date was not checked, the year of the saved revision is used and the `venue` field says so.
- Matrix Olm and Megolm documents carry no date or author in the source; they are attributed to the Matrix.org Foundation with an approximate year.
- Papers announced for 2026 venues (CCS 2026, USENIX Security 2026, ASIACRYPT 2026) are included from their ePrint versions.

## Seeds for other slices

- Blockchain-log messaging: `2026-esposito-verbeth` (ePrint 2026/1606, public blockchain logs as transport, trial decryption, topic rotation) and `2025-zhaisenbayev-ilyazh-web3e2e` (single-author preprint, informal proofs) belong with the blockchain and Bitmessage-heir slices.
- Abuse reporting and franking under sender anonymity: Hecate (ePrint 2021/1686), Asymmetric Message Franking (2019/565, in PB2), further franking papers 2017/664, 2019/016, 2023/332, 2024/1608 and 2025/1872 were not collected.
- Group membership privacy and moderation not collected: ePrint 2025/469 (semi-open chat groups), 2024/455 (anonymous complaint aggregation), 2025/2179 (policy compliant secure messaging), 2022/1643 (traceability only for illegal content).
- Session (Bitmessage heir): ePrint 2025/554 analyses its group chat encryption and finds replay and reordering attacks by a group insider; a Session slice should read it with Quarkslab's audit.
- Mesh and censorship-resistant messaging: ASMesh (ePrint 2023/1053) gives an anonymous Double Ratchet for mesh networks and cites the Bridgefy analyses (Albrecht et al., CT-RSA 2021 and USENIX Security 2022).
- Telegram: ePrint 2022/595 (cryptographic fragility of the Telegram ecosystem) and 2025/451 (analysis of the Telegram key exchange) were not collected.
- Metadata-hiding group primitives that sit between this slice and PB2: Signal private groups (2019/1416, KVAC), membership privacy for ART (2022/046), metadata-hiding MLS (2022/1533).
- Key transparency has a long tail (Merkle^2, OPTIKS, ELEKTRA, Aegon, MINGLE gossip, Consistency-or-Die, Verdict); a dedicated pass could add further split-view detection and gossip work.

## Open gaps

- No source in this slice analyses Bitmessage's own cryptography (static ECIES to the recipient key, ECDSA signatures on every object, address-derived keys); the closest analyses are the Unger et al. SoK (broadcast transport remarks) and the Session, Cwtch and mesh messenger papers. A Bitmessage-specific audit appears to be missing from the literature found here.
- Deniability results (X3DH, PQXDH, K-Waay, Shadowfax, real-world deniability) all assume interactive sessions; none treats deniability of broadcast objects that carry a sender signature, as Bitmessage's do.
- Post-quantum PCS and bandwidth: SPQR, Triple Ratchet, PQ3 and the pq-metric paper quantify the cost for two-party sessions; no source quantifies it for flooded or federated store-and-forward networks where every node replicates each object.
- Group security over unreliable, serverless delivery: fork-resilient CGKA, DCGKA, DeCAF and CoCoA address concurrency and ordering, but formal treatment of CGKA over an anonymous flood (no ordering service, recipient trial decryption) was not found.
- Conversation-level PCS (session handling, cloning, multi-device) is shown to be weaker than protocol-level PCS (Cremers et al. 2022/1710, impossibility results 2024/1886); no study measures how this plays out in real deployments.
- Key transparency designs presume a directory operator; self-certifying address schemes like Bitmessage's have no counterpart in this literature, and DKVE-style decentralised validation is only a first step.
