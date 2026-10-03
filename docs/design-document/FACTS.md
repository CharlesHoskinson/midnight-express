# Shared facts (use these numbers and names exactly; chapters must agree)

The system is called **Midnight Express** (see STYLE.md, 'The name'). Requirement identifiers use the prefix MPE.

## The requirement set
- 624 requirement entries across 12 areas: FMT 60, CRY 46, PUB 53, CON 66, ECO 57, NET 73, PRF 43, STO 42, OPS 57, PRV 44, SEC 42, VER 41.
- Of these, 509 are live requirements (341 for the prototype, 168 for production), 113 restate an obligation owned by another entry, 2 are withdrawn.
- By priority (live): 444 MUST, 49 SHOULD, 16 MAY. 171 depend on a decision that is still open.
- 53 parameters have reconciled prototype and production values; 81 more have the default their area assumes. 28 decisions (DEC-001 to DEC-028) are recorded.
- The prototype core is 137 requirements in six milestones (M0 envelope and recognition, M1 admission and validation, M2 overlay, M3 clients and stores, M4 ledger and fallback, M5 simulator and measurement).
- Ten decision areas: D1 event format; D2 definition of private; D3 publish and subscribe model; D4 sustainable model; D5 performance; D6 storage; D7 infrastructure actors; D8 network tether; D9 threats; D10 build and verification plan.

## Design decisions (reconciled prototype values)
- Transport: sidecar Bus Nodes running GossipSub (v1.2: v1.1 scoring plus IDONTWANT) beside, not inside, the Midnight node. The ledger carries membership, quota roots, batch anchors and a fallback path; event bodies are never in contract state.
- Envelope: sealed body classes of 256 B, 1,024 B, 4,096 B and 16,384 B; 8-byte fixed visible header; 512-byte admission slot; wire lengths 776, 1,544, 4,616 and 16,904 B; payload capacity 86, 854, 3,926 and 16,214 B; maximum GossipSub transmit size 65,536 B.
- Lifetime and retention: 48 hours (172,800 s); optional paid 7-day archive.
- Load: 10 envelopes per second and 64 KiB per second per shard; one shard at launch (benchmarks use 1 and 8).
- Mesh parameters: D = 8, D_low = 6, D_high = 12, D_out = 4; heartbeat 1 s. Edge bandwidth budget 6 Mbit/s per direction.
- Anchors: one per 60-second window, covering all shards; live anchor history 49 hours (2,940 records).
- Admission: per-membership limits by class (64, 16, 4, 1) per 60-second epoch; one nullifier per envelope; restart barrier 140 s; cached roots stop being accepted after 25 hours; stale chain-view threshold 60 s.
- Recognition: salted 16-byte tag per envelope; fuzzy detection clues only for first contact.
- Message identifier: hash of all wire bytes (the envelope identifier, which excludes the admission slot, is used for deduplication, admission binding and anchors).
- Reconciliation: window-level second-source reconciliation by the client; interval default 60 s (measured: 10 to 15 s is better).
- Proof cost used in the prototype: 4.5 ms per verification (synthetic stand-in, not a measured proof system).

## Midnight facts (state which generation)
- Block (slot) time 6 s; finality about 3 blocks (about 18 s). Block usage budget 1,000,000 B per block in the reference parameters; 1,048,576 B per transaction.
- Contract events: the `emit` mechanism in Compact carries a 32-byte name and a 256-byte payload (`Misc`); all fields must be disclosed; the virtual machine silently drops events above 1 KiB; the node does not keep ledger events and the indexer's contract event subscription exposes them from finalized blocks, at least once.
- The node uses libp2p; consensus gossip is wired through the Substrate gossip engine; there is no GossipSub in the node; adding a protocol means forking the node.
- DUST is non-transferable and not usable to pay operators; the unit of paying relays or storage would have to be NIGHT or another mechanism. Midnight transactions have no signer, so per-sender limits must live in contract logic.
- The published documentation describes the earlier ledger generation; the node code pins ledger 9. Always say which.

## Experimental facts (status, binding)
- Throwaway exploratory runs (Rust, rust-libp2p, in-process swarms, a stand-in admission proof, a mock ledger) were used to understand the design and to decide what the proof of concept should be. They are not evidence: nothing in the document rests on them, and their figures appear only in Chapter 10, labelled as unreplicated exploratory observations. There is no proof of concept yet; it is the next step (a single reference implementation with a deterministic simulator, specified in Part III).
- The document never mentions that several implementations were built, compared, judged or selected.
- The ledger interface contracts (Bus Registry, ledger lane, consumer) were compiled with Compact toolchain 0.35.0; circuit sizes come from the compiler's circuit model and fees are derived from the ledger cost model. Nothing ran on a Midnight network.
- Stock rust-libp2p gossipsub 0.50 cannot pin v1.2 on a custom protocol identifier; the default `/meshsub/1.2.0` works. (A fact read from the source.)

## Corrections and additions (binding)
- Transport profile: Midnight Express requires GossipSub v1.2 behaviour (v1.1 scoring and mesh rules plus IDONTWANT). Shard topics and request-response identifiers use `/mpe/<g>/1` (g = first eight bytes of the genesis hash, lowercase hex); the transport profile requires negotiating `/meshsub/1.2.0`; the reference build negotiates `/mpe/<g>/1/gossipsub/1.2.0` through a vendored `Version::V1_2` change and does not interoperate with standard-only peers without configuration. Stock rust-libp2p 0.50 accepts only V1_0 or V1_1 in `protocol_id`.
- Foundation status: only MIP-0002 is Accepted; MIP-0019, MPS-0005, MPS-0007 and MPS-0043 are Proposed. MPS-0005 Part 2 (on-chain private events) is planned and its text is unpublished. Mainnet runs ledger 8.0 (as of 2026-08-04); events arrive with ledger 9; MIP-0002 is live on Stagenet. MIP-0002 and CoIP-0003 are normative for Phase 1 events where MPS-0005 differs.
- Ledger lane capacity is bound by `bytes_written` (50,000 B per block) as well as `block_usage`: about 6.3 class-1 and 1.5 class-2 Messages per second for the whole chain with MIP-0002's 40-byte overhead. The live `block_usage` value (200,000 or 1,000,000) is unmeasured.
- `Misc` names carry a version: `mip-xxxx:anchor[v1]` and `mip-xxxx:envelope[v1]`, NUL-padded to 32 bytes. The 288-byte figure is struct data of a `Misc` event, not its serialized size.
- Bonds are Bus Registry contract balances and have no relation to NIGHT staking.
- Fuzzy detection clues for first contact are not part of the design (DEC-020).
- Ledger interface experiment (Compact 0.35.0, language 0.27.0, ledger-9 rc; nothing run on a network; fees derived): Bus Registry, ledger-lane and consumer contracts compile; `emit` needs ledger 9 (toolchain 0.33+). One `Misc` from 256 bytes needs 166,241 rows (k = 18); four parts k = 20; sixteen parts about k = 22. Proof 4,368 B, verifying key at most 2,119 B for every circuit. Registration about 8.7 KB and 0.246 DUST (0.308 with margin); Anchor post 0.195 DUST (0.244), about 280 DUST per day at one per 60 s; 16 parts in one call 0.188 DUST; 16 separate calls 0.866 DUST. Authority is a hash preimage proved in circuit (no signer); contracts compare but cannot read block time; the 3,600 s root window cannot be enforced by the contract; DUST cannot be paid to a contract; large transcripts land in the fallible segment, so ledger-lane parts are in one phase of one intent, not the guaranteed phase. Full results: `prototype/registry/RESULTS.md`.
