# PB1-bitmessage-heirs: collection notes

Run date 2026-10-01. Catalog: `catalog/PB1-bitmessage-heirs.jsonl` (87 lines: 63 downloaded, 14 metadata_only, 10 duplicate, 0 not_found).

## Hosts and limits met

- OpenAlex: first calls returned 429 "insufficient budget" (shared IP budget, resets 00:00 UTC). It worked again for short stretches later, then failed again. One full-text search for "bitmessage" (102 hits, mostly noise) and a few title/abstract searches got through. Cursor paging beyond that was not possible.
- Semantic Scholar: 429 on every try.
- WebSearch tool: session budget (200 calls) ran out mid-run, so the heirs Dust, Berty, Quiet and Bitchat were fetched by direct URL, not searched.
- GitHub API: 60 calls per hour per IP, used up after about 25 calls. Raw files (`raw.githubusercontent.com`) kept working.
- IACR ePrint: 429 on the PDF host twice, then worked for `2020/1414`.
- University of Texas repository (Krawisz report): 403 (bot wall). Not bypassed.
- ACM Digital Library PDFs: 403 for ASMesh and Amigo. Wiley PDF: 403. IEEE `stampPDF` returned the PDF for the gold-OA IEEE Access paper only.
- `docs.bitmessage.org`: DNS does not resolve. ResearchGate: not used (login or bot wall).
- Ethereum wiki Whisper pages: GitHub wiki pages are deprecated stubs (Wayback copy has no content); the old `devp2p/caps/whisper.md` is gone. EIP-627 plus Waku v1 and the Status specs are the surviving Whisper specifications.

## Queries run (all 2012 onward unless marked)

- arXiv API: `all:bitmessage`, `abs:Bitmessage`, `all:"PyBitmessage"` returned 0 hits (no arXiv paper has Bitmessage in the title or abstract). Phrase scans: anonymous messaging, metadata-private messaging, recipient/receiver anonymity, decentralized messaging blockchain, trial decryption, message detection, oblivious message retrieval, stealth address messaging/scanning, view tag, nostr, ethereum whisper, bridgefy, bluetooth mesh messaging, waku, flood + encrypted messages, PoW + spam + messaging. About 30 distinct results; relevant ones kept.
- Crossref `query.bibliographic`: Bitmessage (3 hits), PyBitmessage, Bitmessage forensic, PyBit Forensic Investigation, Ethereum Whisper messaging, Waku, Nostr, Bluetooth mesh messenger, fuzzy message detection, oblivious message retrieval.
- OpenAlex full text "bitmessage": 102 hits read in full; 9 are real Bitmessage sources; the rest are single-mention noise. Read-through of the full texts I could download (arXiv 1911.08875, 2202.02043, 2509.08248, 2505.02392, 2210.12776, 1409.5841, AMCS 2016, and others) confirmed which actually discuss Bitmessage.
- OpenAlex title/abstract: Bitmessage, PyBitmessage, Ethereum Whisper, Nostr, Waku messaging, Bridgefy, mesh messaging protest, BitChat.
- Text grep over all PDFs and Markdown in `pdfs/` at the end of the run (about 700 files from all slices) for "bitmessage": only the files listed in the catalog, three Unger SoK copies, two BIP-47 copies, Kachina (one-line mention), the Jami DHT notes (one line) and Kwon circuit fingerprinting (one line) contain it.

## Bitmessage proper: what exists

Primary: whitepaper (2012), wiki protocol spec (v3), repository protocol docs (address, encryption, PoW, extended encoding), FAQ, changelog, vendor RCE notice, NVD records for CVE-2018-1000070 (eval injection in 0.6.2, fixed 0.6.3) and CVE-2021-26917, the 2026 post-quantum issue.
Scholarly, in total only seven items address Bitmessage itself:

1. Kovacs, Karakatsanis, Svetinovic, iThings 2014 (requirements case study, metadata only).
2. Lukau, HTW Berlin bachelor thesis 2014 (code review; ResearchGate only, metadata only).
3. Schaub and Rossi, IEEE P2P 2015 (PoW analysis; downloaded from the author page via Wayback).
4. Kobusinska et al., AMCS 2016 (Aldeon; best comparative text on streams and 48-hour retention).
5. Krawisz, UT Austin 2018 (bmd in Go, performance; metadata only).
6. Shi, Guo, Xu, IEEE Access 2021 (Bitmessage Plus).
7. Krause, Choo, Le-Khac, 2022 (PyBitmessage forensics; metadata only).

Plus theory and design that name Bitmessage as the flooding baseline: Erturk and Xu 2019, Upadhyay (EFPIX) 2025, Kopyciok et al. 2025 (SMSG in Particl/BasicSwap).
No security audit of PyBitmessage was found; the wiki main page itself states one is needed.

## Mentions only (not catalogued)

- Nelson and Askarov, "With a Little Help from My Friends" (arXiv 2202.02043): one sentence, says Bitmessage and Riposte broadcast to subscribers and give no sender deniability.
- Nelson and Pagnin, "Metadata Privacy Beyond Tunneling" (arXiv 2210.12776): table row only.
- Noyen et al., "When Money Learns to Fly" (arXiv 1409.5841): one sentence.
- Mott 2018 (Twister, Studies in Conflict and Terrorism) and Gräml 2025 (P2P forensics bachelor thesis): one mention each in the full text. Other OpenAlex full-text hits (Weimann 2015, Platzer 2021, and similar) were not opened.
- Kwon et al. (USENIX Security 2015): Bitmessage listed as a Tor-only service.

## Heirs and relatives: what was collected

- Whisper: EIP-627, Status specs 3, 4, 5, 10, Waku v1 (6/WAKU1), 8/WAKU-MAIL, three small application papers (Korean journal, covert-channel paper, dApp paper; all closed, metadata only). No independent security analysis of Whisper was found; the Waku family documents state why Whisper was dropped (bandwidth, Bloom-filter leak, PoW).
- Waku: 10, 11, 12, 13, 14, 17, 19, 26, 53, RLN v1 and v2, Noise/X3DH ratchet, gossipsub-tor-push, Dandelion, libp2p-mix, stealth commitments, adversarial models; papers `2022-taheri-waku-rln-relay`, `2022-thoren-waku`, `2022-taheri-spam-protected-gossip` are already in slice C (duplicate lines).
- Swarm PSS: pss README, Book of Swarm (section 4.4, Trojan chunks), whitepaper v1.0.
- Nostr: NIP-01, 04, 13, 17, 44, 59; Kimura et al. attacks (EuroS&P 2025, paywalled); Wei and Tyson relay measurement (arXiv).
- Bitchat and BLE mesh: bitchat whitepaper v2.0 and source-routing doc, Firmansyah forensic study, Biagioni review (paywalled), Bridgefy break (2021), ASMesh and Amigo (ACM, 403), FoSAM; Bridgefy-again and Perry mesh anonymity are catalogued by other slices (duplicate lines).
- Note scanning: Zcash protocol specification, ZIP-307, Penumbra FMD chapters; FMD, FMD false-positives and OMR are already in `pdfs/` from another slice (duplicate lines); added Frank et al. (altruism game) and Kovacs and Seres (Umbra anonymity).
- Berty (Wesh protocol page), Quiet (README).
- Forks and rewrites: bmd (Go), MiNode (Python 3, I2P), PyBitmessage-I2P, Ripple (Rust, libp2p), a Python 3 PyQt5 port, a 2026 Rust-over-Tor client; Particl SMSG appears via the Monero P2P exchange paper and the Particl Academy page (the page itself was not saved because it is product documentation without a date).

## Wanted but not obtained

- Lukau thesis PDF (ResearchGate only). Ask the author or HTW.
- Krawisz report PDF (UT repository bot wall). Try the author or a mirror later.
- Kimura et al., "Not in the Prophecies" (IEEE). No open copy found; check IACR ePrint by hand.
- ASMesh and Amigo PDFs (try ePrint search from a browser).
- Biagioni, Krause, Kovacs et al., Zhang et al., Lee et al., Abdulaziz et al.: paywalled.
- "Dust": no source identified. The name is ambiguous and the search budget ran out. If the owner means a specific project, give a URL.
- A Whisper security analysis (none located), a Waku audit report, and independent audits of bitchat or Berty.
- Bleep, ShadowChat (Shadowcash chat, called a "clone" of Bitmessage by Kobusinska et al.), Twister, the Bitseal/Jabit Java clients, bmgo and the Mailchuck fork have no design documents located.

## Overlap with other slices (same sources, different slugs)

The shared `pdfs/` folder already held copies of several of these sources when I catalogued: EIP-627 (`2015-eip627-whisper`, `2017-eip627-whisper`), Zcash protocol spec (`2016-zcash-protocol-spec.pdf`, byte-identical to my `2016-hopwood-zcash-protocol-spec.pdf`), ZIP-307 (`2018-zcash-zip307`, `2020-zip307-light-client`), Penumbra FMD (`2022-penumbra-fmd`), Waku/RLN specs (`2020-waku-message`, `2020-waku-relay`, `2020-waku2-spec`, `2022-waku-rln-relay-spec`, `2022-waku-x3dh-sessions`, `2025-waku-dandelion-spec`, `2025-waku-mix-spec`, `2024-waku-rln-stealth-commitments`, and more), NIP-13 (`2020-nip13-pow`), BIP-47 (two copies), Unger SoK (three copies). The lead should dedupe by source URL.

## Seeds for other slices

- Bitmessage-derived and Bitmessage-using systems: Particl SMSG (design docs in particl-core, not found), BIP-47 notification over Bitmessage, ShadowChat.
- Receiver-side scanning cost: Group OMR, PerfOMR, HomeRun, SophOMR and Snake-eye papers are in `pdfs/` from other slices; Monero view tags (MRL-0073) and BIP-352 silent payments are the same problem on payment chains.
- Open questions for the review: (1) Bitmessage has no measured network study (node count, bandwidth per stream, delivery latency) beyond Krawisz's bmd benchmark; (2) no formal anonymity analysis of the flood-and-decrypt model exists except the game-theoretic bounds of Erturk and Xu; (3) the tension between topic-based interest filters (Whisper Bloom, Waku filter/store, Nostr relay filters) and recipient ambiguity is stated in the specs but never quantified in the literature found.
