# MPE prototype proposal

A Rust proof of concept of the Midnight Private Events (MPE) bus on rust-libp2p GossipSub v1.1, sized for a builder to implement in about two hours. Every value below is the Prototype value from `design/ears/RECONCILE.md` (parameter table and decision register DEC-001 to DEC-028) unless the text marks it as a prototype engineering choice. Requirement IDs refer to `design/rounds/r5/e*.md` as corrected by RECONCILE.md; the build order and the proving test of each core requirement are in `design/ears/POC_CORE.md`. Midnight paths are relative to `/home/charl/midnight/`; libp2p paths to `/home/charl/libp2p/`.

## 1. Purpose and what it must teach

The prototype exists to measure the reconciled design against its own numbers and to break it on purpose. It is not a product. It must produce evidence on five questions that no amount of review can settle:

1. **Does the wire format hold its privacy claims in running code?** Four fixed wire sizes (776, 1,544, 4,616 and 16,904 B), no plaintext field visible to a relay, no value constant per publisher in the Admission Slot, and recognition that sends nothing back into the network (DEC-003, DEC-013).
2. **Does the validation pipeline defend the mesh without punishing honest peers?** Strict application validation before forwarding, the Reject/Ignore split, the wire-byte message id against duplicate-cache censorship (DEC-010), stale-chain behaviour (DEC-009), the restart barrier (DEC-017), equivocation handling (DEC-014) and the per-class quota (DEC-016).
3. **What does the design cost?** Per-node bandwidth per direction against the 6 Mbit/s edge budget (DEC-027), CPU per validated Envelope, recognition CPU per key (DEC-003), Subscriber download per day (DEC-021), store bytes per retained hour (DEC-004), reconciliation overhead (DEC-025).
4. **Do the off-overlay paths compose?** Back-fill and reconciliation from Store Nodes of distinct Operators, Anchors over 60 s windows with an inclusion proof a contract consumer verifies (DEC-022, DEC-024), and the labelled ledger fallback under Midnight's real `Misc` and block limits (DEC-008).
5. **Which requirements are wrong?** Section 13 lists the requirement texts that the byte layout and the rust-libp2p API already contradict; the runs must confirm or refute each.

The learning agenda with decision rules is `design/prototype/LEARNING_QUESTIONS.md`; the pass/fail gates are `design/prototype/thresholds.json`.

## 2. Architecture

```
                 out-of-band invitation (stream secret, publisher keys, network, profile)
   +-------------+ ----------------------------------------------------------+
   | Publisher   |                                                           v
   | (mpe-client)|  publish req (Envelope)    +------------------------------------------+
   |  seal, tag, |--------------------------->|  Bus Node (ingress, chosen at random     |
   |  admission  |<--- acceptance {EID} ------|  from 2 dialled)  mpe-node              |
   +-------------+      (NET-049)             |   Validator -> gossipsub.publish(shard)  |
          |                                   +--------------------+---------------------+
          | ledger fallback (opt-in only)                          | GossipSub v1.1 mesh, topic
          | Misc parts in one intent                               | /mpe/<g>/1/shard/<i>
          v                                                        v  (D,D_lo,D_hi,D_out)=(8,6,12,4)
   +--------------+   finalized blocks   +-----------+   +---------+   +---------+   +-------------+
   | MockLedger   |--------------------->|MockIndexer|   |Bus Node |<->|Bus Node |<->| Store Node  |
   | Registry:    |   contractEvents     |(finalized |   |validate |   |validate |   | (Bus Node + |
   |  roots,relay |   (address filter)   | only)     |   |forward  |   |forward  |   |  Store)     |
   |  list,params,|                      +-----+-----+   +----+----+   +----+----+   +------+------+
   |  Anchors     |<-- Anchor tx (60 s) -------|--------- anchorer (one Bus Node)           |
   | MockContract |                            |              |  feed pull 1 s (NET-048)   | back-fill,
   +------^-------+                            |              v                            | inventory,
          |                                    |     +------------------+  reconcile 60 s | receipts
          | reaction tx (signature, nullifier, +---->| Subscriber       |<----------------+
          |   optional inclusion proof)              | (mpe-client)     |
          +------------------------------------------| tag test, open,  |--> Consumer: agent callback,
                                                     | dedup, labels    |    wallet adapter, contract
                                                     +------------------+    reaction builder
```

### 2.1 Components

| Component | Role | Code |
|---|---|---|
| Publisher | Seals an Event into a fixed-size Envelope, attaches the Admission Proof, submits to one Bus Node chosen at random from two it dialled (MPE-NET-033), retries identical bytes (MPE-PUB-023) | `mpe-client::publisher` |
| Bus Node | Sidecar process (MPE-NET-001a). Joins one GossipSub topic per Shard, runs the application validator on every Envelope before forwarding, serves the Shard feed to non-mesh clients | `mpe-node` |
| Store Node | Bus Node with the store role. Retains every Envelope it Accepts until its visible expiry, answers back-fill, inventory and receipt requests | `mpe-node` + `mpe-core::store` |
| Anchorer | Bus Node with the anchorer role. Builds per-window batch roots and submits one Anchor per non-empty 60 s window | `mpe-node::anchorer` |
| Bootstrapper | Bus Node with mesh degree 0 (MPE-NET-024 profile); used only for initial dials | `mpe-node` |
| Subscriber | Receives the complete Shard (embedded in a Bus Node or by feed pull), tests every Envelope against its recognition keys locally, opens and authenticates matches, deduplicates, labels | `mpe-client::subscriber` |
| Consumer adapters | Agent (async callback), wallet (stream grant stub), contract (reaction transaction builder) | `mpe-client::consumer` |
| MockLedger | Midnight stand-in: 6 s blocks, 3-block finality, block and transaction byte limits, `Misc` events, no signer; hosts the mock Registry and the mock contract | `mpe-core::ledger` |
| MockIndexer | `contractEvents`-shaped read path over finalized blocks only | `mpe-core::indexer` |
| Simulator | Runs 50 to 200 real swarms in one process, drives scenarios, measures, writes the result JSON | `mpe-sim` |

### 2.2 Data flow: Publisher to Subscriber

1. **Seal** (Publisher). Pick the smallest class that holds the payload (MPE-FMT-014). Draw salt (16 B) and nonce (12 B) from the OS RNG. Derive the per-Envelope encryption key from the stream secret and salt, compute the 16 B Tag, sign the statement (MPE-CRY-021), encrypt Sealed Prefix, authentication block, payload and zero padding (section 4).
2. **Identify.** Compute the Envelope Identifier (EID) over the domain string, Network Identifier, header bytes 0-7 and the Sealed Body (MPE-FMT-018). Construction is body, then EID, then Admission Slot (MPE-FMT-020).
3. **Admit.** Compute epoch, nullifier, share and proof for one unused credit index of the size class (section 6) and write the 512 B Admission Slot.
4. **Submit.** Send the Envelope to one Bus Node over `/mpe/<g>/1/publish`. The Bus Node runs the full validator; on Accept it calls `gossipsub.publish` on the Shard topic and returns `Accepted{eid}`. On Reject or Ignore it returns nothing; the client waits P-PUB-5 = 5 s, then sends the identical bytes to another Bus Node, at most P-PUB-6 = 3 Bus Nodes, and stops once the admission epoch ended more than 20 s ago (MPE-PUB-053).
5. **Propagate.** Each Bus Node receives the GossipSub message, computes the message id as SHA-256 over the wire bytes (DEC-010), holds it until its validator returns Accept, Reject or Ignore, and forwards only on Accept (MPE-NET-015).
6. **Feed.** A remote Subscriber pulls `/mpe/<g>/1/feed` from one Bus Node every P-PUB-2 = 1 s and receives every Envelope that Bus Node Accepted on the requested Shard (MPE-NET-048); its deliveries carry the `gateway` carrier attribute, the Bus Node stream service being the gateway path of DEC-008. A Subscriber embedded in a Bus Node's process reads that node's Accepted stream directly and its deliveries carry `overlay`. The simulator runs half of its Subscribers each way.
7. **Recognise and open.** For every Envelope the Subscriber evaluates the Tag under each of its recognition keys (at most 256). A match is only a candidate (MPE-CRY-014): the client opens the AEAD, checks padding, the Sealed Prefix, the signature against the invitation's authorized keys and the expiry, then delivers (MPE-CRY-022). Unmatched bytes are discarded.
8. **Deduplicate and label.** At most one delivery per EID and per (publisher, Logical Event Identifier) (MPE-PUB-036, MPE-PUB-037). Each item carries exactly one finality label (`gossip` or `final`), one carrier attribute (`overlay`, `gateway`, `ledger`) and the `stored` attribute when three Operators' receipts validate (DEC-026).
9. **Repair.** Every P-PUB-3 = 60 s the client compares its received EIDs against the inventory of a Store Node run by a different Operator and back-fills any window that contains a missing EID (MPE-PUB-014, MPE-PUB-015).

### 2.3 Data flow: to a contract consumer

1. The anchorer collects the EIDs it Accepted per Shard, assigned to 60 s windows by `window = floor((expiry - 172,800) / 60)`, so every node assigns an Envelope to the same window (section 9). Twenty seconds after a window closes it builds the per-Shard batch roots and the window root and submits one Anchor transaction to the mock Registry.
2. After 3 blocks (18 s) the Anchor is final. A Subscriber marks an Event `final` once it verifies the Event's inclusion under a finalized Anchor (MPE-CON-016).
3. An application that wants a contract to react calls the reaction builder explicitly. The builder produces a MockLedger transaction to the target mock contract carrying the publisher statement, its Ed25519 signature, a secret-derived consumption nullifier (MPE-CRY-025) and, optionally, the inclusion proof. The mock contract checks the publisher set, destination, action, expiry and nullifier, and inserts the nullifier atomically with its effect.

## 3. Crate layout and public traits

Workspace layout follows `design/prototype/BUILD_BRIEF.md`:

```
mpe-core/      wire.rs (header, classes, offsets)   seal.rs (Sealer)        tag.rs (TagScheme)
               keys.rs (stream secrets, HKDF, invitations)                   admission.rs (AdmissionProof, StandInRln)
               validator.rs (Validator, outcomes)   seen.rs (seen-set, nullifier cache, evidence)
               store.rs (Store, MemStore)           anchor.rs (RFC 6962 Merkle, Anchor payload, proofs)
               ledger.rs (LedgerAdapter, MockLedger, mock Registry, MockContract)
               indexer.rs (Indexer, MockIndexer)    clock.rs (Clock, SimClock)   outcome.rs (closed outcome set)
               vectors/*.json                       tests/independent_decoder.rs
mpe-node/      config.rs (GossipSub + scoring)      behaviour.rs (gossipsub + request-response protocols)
               node.rs (event loop, verify scheduler, eviction)   protocols.rs (codecs)   anchorer.rs   main.rs
mpe-client/    publisher.rs  subscriber.rs (recognition, dedup, gaps, labels, reconciliation)
               consumer.rs (agent, wallet, contract reaction builder)   fallback.rs (ledger carrier)
mpe-sim/       main.rs (clap)  harness.rs (swarms)  transport.rs (counting memory transport)
               schedule.rs  capture.rs  metrics.rs  scenarios/{baseline,spam,...,fallback}.rs
```

The skeleton in `design/prototype/skeleton/` builds a swarm with `MessageAuthenticity::Signed` and `ValidationMode::Strict`. The prototype replaces both with `Anonymous` (MPE-NET-009a); keeping the skeleton's settings would put the Bus Node's PeerId and a signature on every Envelope.

### 3.1 Traits

All traits are object-safe and synchronous. Ledger-facing traits read a cache that a background task refreshes from finalized state, which is also the behaviour DEC-009 requires under a stale view; a devnet adapter implements the same traits with a network-backed cache.

```rust
pub type UnixSecs = u64;
pub struct Eid(pub [u8; 32]);
pub struct NetworkId(pub [u8; 32]);           // Midnight genesis hash (mock: fixed constant)

/// Admission Proof: one rate-limited publication. A real RLN prover and verifier implement the
/// same trait; the stand-in is section 6.
pub trait AdmissionProof: Send + Sync {
    /// Bytes of the proof field inside the 512 B Admission Slot (stand-in and Waku RLN: 256).
    fn proof_len(&self) -> usize;
    /// Client side. Fails with NotReady if the credit index is exhausted or the root is unknown.
    fn prove(&self, w: &AdmissionWitness, p: &AdmissionPublic) -> Result<Vec<u8>, AdmissionError>;
    /// Bus Node side. Pure function of public inputs, proof bytes and Registry context.
    fn verify(&self, p: &AdmissionPublic, proof: &[u8], ctx: &RegistryView) -> ProofVerdict;
}
pub struct AdmissionPublic { pub network: NetworkId, pub epoch: u64, pub root: [u8; 32],
    pub nullifier: [u8; 32], pub share_y: [u8; 32], pub size_class: u8, pub eid: Eid }
pub struct AdmissionWitness { pub secret: Scalar, pub leaf_index: u32, pub credit_index: u16,
    pub limits: [u16; 4], pub path: MerklePath }
pub enum ProofVerdict { Valid, Invalid, OverQuota /* stand-in only, see 6.3 */, UnknownRoot }

/// Overlay and client view of Midnight. Every read is from finalized blocks (MPE-NET-036).
pub trait LedgerAdapter: Send + Sync {
    fn finalized_head(&self) -> Result<BlockRef, LedgerError>;               // height, time, hash
    fn membership_roots(&self) -> Result<Vec<RootRecord>, LedgerError>;      // root, period, published_at, superseded_at
    fn historic_root(&self, root: &[u8; 32]) -> Result<Option<RootRecord>, LedgerError>; // MPE-NET-056
    fn relay_list(&self) -> Result<Vec<RelayEntry>, LedgerError>;            // MPE-NET-054
    fn registry_params(&self) -> Result<RegistryParams, LedgerError>;        // shard count, max version, bootstrap hash
    fn anchors(&self, from_window: u64) -> Result<Vec<AnchorRecord>, LedgerError>;
    fn bus_paused(&self) -> Result<bool, LedgerError>;
    fn ledger_parameters(&self) -> Result<LedgerParams, LedgerError>;
    fn submit(&self, tx: MockTx) -> Result<TxTicket, LedgerError>;          // Registry calls, Misc carriage, reactions
    fn tx_status(&self, t: &TxTicket) -> Result<TxStatus, LedgerError>;      // Pending, Included(h), Final(h), Failed
    fn staleness(&self, now: UnixSecs) -> Staleness;                        // MPE-NET-019: Fresh | Stale
}

/// Read path for ledger-carried events: the shape of the Indexer `contractEvents` subscription.
pub trait Indexer: Send + Sync {
    /// Events of one contract with id >= from_id, finalized blocks only, at most `limit`
    /// (clamped to 1..=500, default 100), ascending id. At-least-once across calls.
    fn contract_events(&self, contract: &ContractAddress, from_id: u64, limit: u16)
        -> Result<Vec<ContractEvent>, IndexerError>;
    fn retention_coverage(&self) -> Coverage;                               // Unknown in the mock
}

/// Envelope retention on a Store Node.
pub trait Store: Send {
    fn admit(&mut self, env: &[u8], eid: &Eid, now: UnixSecs) -> Result<UnixSecs, StoreError>; // returns deadline
    fn page(&self, shard: u8, from: Cursor, until: UnixSecs, limit: usize) -> Result<Page, StoreError>;
    fn inventory(&self, shard: u8, w: TimeWindow, after: Option<Eid>, limit: usize) -> Result<InvPage, StoreError>;
    fn get(&self, eid: &Eid) -> Result<Option<Vec<u8>>, StoreError>;
    fn prune(&mut self, now: UnixSecs) -> usize;
    fn bytes(&self, shard: u8) -> u64;
}

/// Sealing under the version-1 profile (MPE-CRY-001).
pub trait Sealer {
    fn seal(&self, keys: &StreamKeys, ev: &EventIn, hdr: &HeaderPrefix, rng: &mut dyn CryptoRngCore)
        -> Result<SealedBody, SealError>;                                   // TooLarge, RandomnessUnavailable
    fn open(&self, keys: &StreamKeys, hdr: &HeaderPrefix, body: &[u8]) -> Result<OpenedEvent, OpenError>;
}

/// Recognition material in the Sealed Body clear prefix (MPE-FMT-051, MPE-CRY-013).
pub trait TagScheme {
    fn tag(&self, rec: &RecognitionKey, network: &NetworkId, salt: &[u8; 16]) -> [u8; 16];
    /// Constant-time comparison against every installed key; returns candidate streams only.
    fn candidates(&self, ring: &KeyRing, body: &[u8]) -> SmallVec<[StreamId; 2]>;
}

/// Application validator. `precheck` is cheap and synchronous; `finish` consumes the proof verdict.
pub trait Validator {
    fn precheck(&mut self, msg: &Inbound<'_>, now: UnixSecs) -> Precheck; // Done(Outcome) | NeedsProof(Job)
    fn finish(&mut self, job: Job, verdict: ProofVerdict, now: UnixSecs) -> Outcome;
}
pub enum Outcome { Accept(Eid), Reject(RejectReason), Ignore(IgnoreReason) }
```

`Inbound` carries the wire bytes, the topic's version and Shard index, the propagation source and whether the bytes came from GossipSub or from a client publish request. The client library reports every refusal or failure as one of the 19 names of MPE-CON-056 (`TooLarge`, `NotReady`, `NotAccepted`, `Busy`, `Refused`, `ResourceExhausted`, `StorageExhausted`, `KeyLimit`, `Degraded`, `SourceFailed`, `Unresolved`, `RetentionGap`, `KeyGap`, `CorruptRecord`, `LedgerUnavailable`, `LedgerPaused`, `BusPaused`, `InsufficientDust`, `SessionUpdateRequired`).

## 4. Envelope and sealing

### 4.1 Size classes

| Class | Sealed Body B | Wire = 8 + 512 + B | Payload capacity B − 170 | Misc parts 4^c | Envelopes/s at 64 KiB/s |
|---|---|---|---|---|---|
| 0 | 256 | 776 | 86 | 1 | 10.00 (count cap binds) |
| 1 | 1,024 | 1,544 | 854 | 4 | 10.00 |
| 2 | 4,096 | 4,616 | 3,926 | 16 | 10.00 |
| 3 | 16,384 | 16,904 | 16,214 | 64 | 3.88 |

Payload larger than 16,214 B returns `TooLarge` before any admission work (MPE-FMT-015). Every class fits under the 65,536 B GossipSub transmit cap with framing.

### 4.2 Wire layout (big-endian, MPE-FMT-002; offsets from the first wire byte)

| Offset | Length | Field | Rule |
|---|---|---|---|
| 0 | 1 | `version` | 1; bound to the topic (MPE-FMT-023) and to exactly one profile (MPE-FMT-053) |
| 1 | 1 | `size_class` | 0-3; other values Reject (MPE-FMT-008) |
| 2 | 1 | `shard` | equals the topic's Shard index (MPE-FMT-052) |
| 3 | 1 | `reserved` | 0 (MPE-FMT-006) |
| 4 | 4 | `expiry` | u32 Unix seconds; honest publishers set creation time + 172,800 (4.5) |
| 8 | 8 | epoch | `floor(unix / 60)` (MPE-ECO-053) |
| 16 | 32 | membership root | current or superseded less than 3,600 s ago |
| 48 | 32 | nullifier | section 6 |
| 80 | 32 | share y | section 6 |
| 112 | 256 | proof | stand-in: section 6.2 |
| 368 | 152 | zero fill | non-zero byte: Reject (MPE-FMT-050) |
| 520 | 16 | salt | Sealed Body clear prefix (MPE-FMT-051) |
| 536 | 12 | AEAD nonce | |
| 548 | 16 | Tag | |
| 564 | B − 44 | ciphertext | ChaCha20-Poly1305 output including the 16 B authenticator at its end |

Sealed plaintext (length B − 60), offsets inside the plaintext:

| Offset | Length | Field |
|---|---|---|
| 0 | 1 | `pt_version` = 1 |
| 1 | 1 | `kind` = 1 (application Event); 2 reserved for control; no receipt kind (MPE-FMT-036) |
| 2 | 2 | `flags`, bit 0 = authentication block present (always 1 in version 1) |
| 4 | 2 | `payload_len` |
| 6 | 2 | `schema_version` |
| 8 | 8 | `seq`, per publisher and stream, +1 per Event (MPE-PUB-019) |
| 16 | 16 | Logical Event Identifier, random, identical on every retransmission and carrier (MPE-FMT-022) |
| 32 | 8 | schema id |
| 40 | 2 | authorized-key index into the invitation's publisher key list (MPE-CRY-041) |
| 42 | 4 | creation time, u32 Unix seconds |
| 46 | 64 | Ed25519 signature over the statement of 4.4 |
| 110 | `payload_len` | payload (canonical CBOR by default; the schema decides) |
| 110 + `payload_len` | rest | zero padding; any non-zero pad byte: discard as malformed (MPE-FMT-017) |

### 4.3 Keys, Tag and nonce rules

Profile `mpe-v1-sym`: HKDF-SHA-256, HMAC-SHA-256, ChaCha20-Poly1305 and plain Ed25519 (MPE-CRY-001), all from the crates in the build brief. `N` is the 32 B Network Identifier; `S` the 32 B stream secret from the OS RNG (MPE-CRY-008), which is also the audience key (RECONCILE duplicate row for MPE-CRY-008).

| Value | Derivation |
|---|---|
| recognition key `k_rec` | `HKDF-SHA-256(salt = N, ikm = S, info = "mpe/v1/rec" ‖ profile_id)`, 32 B |
| Tag | `HMAC-SHA-256(k_rec, "mpe/v1/tag" ‖ N ‖ salt)[0..16]` |
| encryption key `k_enc` | `HKDF-SHA-256(salt = envelope salt, ikm = S, info = "mpe/v1/enc" ‖ N ‖ profile_id)`, 32 B, one per Envelope |
| nonce | 12 B from the OS RNG, carried in the clear prefix |
| stream id | `SHA-256("mpe/v1/stream" ‖ S)`; sealed context only, never on the wire |
| Shard | `u64_be(SHA-256("mpe/v1/shard" ‖ S)[0..8]) mod P-PUB-1` (MPE-PUB-002 as corrected) |
| event secret | `HKDF-SHA-256(salt = N, ikm = S, info = "mpe/v1/event" ‖ LEI)`, input to the consumption nullifier |
| EID | `SHA-256("midnight-pe/id/v1" ‖ N ‖ wire[0..8] ‖ Sealed Body)` (MPE-FMT-018; slot excluded) |
| GossipSub message id | `SHA-256("mpe/v1/msgid" ‖ wire bytes)` (MPE-NET-010, DEC-010) |

**Nonce uniqueness (MPE-CRY-010).** Each `k_enc` encrypts exactly one plaintext, because the 16 B salt is fresh per Envelope; a repeated (key, nonce) pair needs a salt collision (probability about 2^-128 per pair). A retransmission sends the identical stored bytes and never re-encrypts (MPE-PUB-023). Nothing depends on a counter, so restored client state cannot cause reuse.

**Recognition (DEC-003 prototype default (d)).** For each Envelope the Subscriber computes one HMAC per installed key and compares in constant time (`subtle`-style comparison from the `hmac` crate's `verify_truncated_left`). Precomputing each key's inner and outer HMAC state makes one evaluation two SHA-256 compressions. At the 256-key cap and 10 Envelopes/s that is 2,560 evaluations per second. A `--recognition trial` client mode skips the Tag and attempts the AEAD open under every key, for the DEC-003 comparison.

### 4.4 Associated data and the signed statement

- AEAD associated data: `"mpe/v1/aad" ‖ N ‖ wire[0..4] ‖ salt ‖ nonce ‖ Tag`.
- Signed statement (MPE-CRY-021): `"mpe/v1/sig" ‖ N ‖ SHA-256(N ‖ wire[0..4] ‖ salt ‖ nonce ‖ Tag) ‖ stream id ‖ LEI ‖ seq ‖ schema id ‖ schema_version ‖ creation ‖ expiry ‖ SHA-256(payload) ‖ destination contract (32 B, zero if none) ‖ action (32 B, zero if none)`.

This departs from the corrected MPE-CRY-004, which binds header bytes 0 to 7. The ledger carrier transmits only the Sealed Body (MPE-FMT-041), so a ledger reader cannot know `expiry` before it decrypts, and MPE-FMT-037 and MPE-FMT-051 require the ledger copy to open exactly as the overlay copy. Bytes 0-3 are reconstructible on both carriers (`version` from the `Misc` name, `size_class` from the part count, `shard` from the audience key, `reserved` = 0). `expiry` stays bound twice without the AAD: the EID covers bytes 0-7 and the admission share is a function of the EID, so a relay that alters `expiry` produces a Reject; and the signed statement contains `expiry`, so a recipient compares the signed value with the visible one. The change is requirement finding F1 in section 13.

### 4.5 Expiry rule

Honest publishers set `expiry = creation + 172,800` (P-FMT-3, the single Prototype lifetime, DEC-004). A ledger reader then reconstructs `expiry`, the statement and the EID from the authenticated creation time. Bus Nodes enforce only the bounds (MPE-FMT-029, MPE-FMT-030); a shorter lifetime needs a sealed `expiry` field (4 B, payload capacity B − 174), which is finding F1.

## 5. GossipSub configuration

rust-libp2p 0.57 with `libp2p-gossipsub` 0.50 (cached crate; the local source tree under `/home/charl/libp2p/rust-libp2p` is 0.51.0 and is the citation target below).

### 5.1 Topics and protocols

- Network prefix `<g>` = the first 8 bytes of the genesis hash in lower-case hex; topic names `/mpe/<g>/1/shard/<i>` for `i` in `0..P-PUB-1` (MPE-NET-006, MPE-NET-031), `IdentTopic`. Prototype: 1 operating Shard; `--shards 8` runs the benchmark topology (DEC-011).
- Request-response protocols, each with a length-prefixed `ciborium` codec and a 65,536 B frame cap: `/mpe/<g>/1/publish`, `/feed`, `/backfill`, `/inventory`, `/receipts`, `/anchor-leaves`, `/inclusion`.
- Transport: TCP, Noise, Yamux (MPE-NET-007); the simulator uses the memory transport with the same Noise and Yamux upgrades (section 11).

### 5.2 Router settings

| Setting | Value | Source |
|---|---|---|
| `MessageAuthenticity` / `ValidationMode` | `Anonymous` / `Anonymous`: `from`, `seqno`, `signature`, `key` absent; messages carrying them are dropped by the codec (MPE-NET-009a/b) | `rust-libp2p/protocols/gossipsub/src/config.rs:40-48` |
| `validate_messages()` | on: nothing is forwarded until `report_message_validation_result` returns Accept (MPE-NET-015) | `behaviour.rs:949` |
| `message_id_fn` | SHA-256 over `"mpe/v1/msgid"` and `message.data` | DEC-010 |
| `mesh_n`, `mesh_n_low`, `mesh_n_high`, `mesh_outbound_min` | 8, 6, 12, 4; `--mesh 6,5,12,2` for the MPE-PRF-010 comparison | DEC-012; defaults 6, 5, 12, 2 at `config.rs:83-86` |
| `heartbeat_interval`, `gossip_factor`, `prune_backoff` | 1 s, 0.25, 60 s | RECONCILE parameter table |
| `flood_publish` | false (default is true at `config.rs:548`) | MPE-NET-013 |
| `max_transmit_size` | 65,536 B | `protocol.rs:100`; MPE-NET-014 |
| `duplicate_cache_time` | 60 s (default, `config.rs:524`); the application seen-set covers the rest of the lifetime | MPE-PUB-027 |
| `idontwant_message_size_threshold` | 1,000 B (P-NET-18); `--idontwant off` sets it to 65,537 so no IDONTWANT is sent | `config.rs:563`; MPE-NET-047 |
| `history_length`, `history_gossip` | 5, 3 (defaults) | |
| `do_px` | on for bootstrappers only | MPE-NET-024 |

rust-libp2p inserts the message id into its duplicate cache before application validation (`behaviour.rs:1983`) and sends IDONTWANT for it before validation (`behaviour.rs:1969`). With the wire-byte id, a copy with a corrupted Admission Slot has its own id and cannot suppress the honest copy (MPE-SEC-042). `--msgid eid` switches to the EID as message id, only for the learning run that reproduces the attack.

### 5.3 Application validator order

The order puts every check that needs no state or cryptography first (MPE-FMT-009, MPE-ECO-013). Rejects are reserved for proven invalidity independent of chain state (MPE-NET-016); while the Ledger Adapter view is stale (local clock and finalized block time differ by more than P-NET-13 = 60 s, MPE-NET-019) every chain- or clock-dependent Reject becomes Ignore (MPE-NET-018, MPE-FMT-031).

| # | Check | Failure outcome | Requirement |
|---|---|---|---|
| 0 | RPC size ≤ 65,536 B; no `from`/`seqno`/`signature`/`key` | dropped by rust-libp2p; P4 on the sender for signed fields | MPE-NET-014, MPE-NET-009b |
| 1 | Per peer per Shard ≤ 20 Envelopes/s (token bucket, burst 20) | Ignore, before any verification | MPE-NET-023 |
| 2 | length ≥ 8; `version` = topic version | Reject | MPE-FMT-023 |
| 3 | `reserved` = 0 | Reject | MPE-FMT-006 |
| 4 | `size_class` ≤ 3 | Reject | MPE-FMT-008 |
| 5 | length = 520 + B[class] | Reject | MPE-FMT-007 |
| 6 | `shard` = topic Shard | Reject | MPE-FMT-052 |
| 7 | `expiry` ≤ clock + 172,800 + 60 | Reject (Ignore if stale) | MPE-FMT-029, MPE-FMT-031 |
| 8 | `expiry` ≥ clock − 60 | Ignore | MPE-FMT-030 |
| 9 | slot bytes 360-511 are zero | Reject | MPE-FMT-050 |
| 10 | compute EID; EID in seen-set | Ignore (duplicate) | MPE-PUB-028 |
| 11 | restart barrier active (5.4) | Ignore | MPE-STO-015 |
| 12 | Bus Node clock inside `[60·epoch − 20 s, 60·(epoch + 1) + 20 s)` | Ignore | MPE-ECO-014 |
| 13 | root is current or superseded < 3,600 s ago; its membership period ended < 3,600 s ago | Ignore | MPE-ECO-015, MPE-ECO-051 |
| 14 | nullifier seen with the same EID | Ignore (duplicate) | MPE-ECO-013 |
| 15 | per-peer queue < 8 jobs and node queue < 128 jobs | Ignore; `Busy` to a publishing client | MPE-SEC-009, MPE-PRF-034 |
| 16 | proof verification (round-robin across peer queues) | Reject; stand-in over-quota index: Reject counted `over_quota` | MPE-ECO-012, MPE-ECO-016, MPE-SEC-010 |
| 17 | nullifier seen with a different EID and the proof is valid | Ignore; store both Envelopes as equivocation evidence; emit `AdmissionConflict` | MPE-ECO-020 (DEC-014) |
| 18 | Accept: insert EID into the seen-set (only now, MPE-SEC-041), nullifier into the nullifier cache, hand to store and anchorer | Accept | |

No step reads the Sealed Body beyond hashing it (MPE-FMT-011). The seen-set keeps an EID until its expiry + 60 s (MPE-PUB-027); the nullifier cache keeps entries 140 s (P-ECO-7). A different-EID nullifier conflict is verified before it is recorded, so a forged slot cannot plant evidence against an honest member.

### 5.4 Restart barrier

After every process start the Bus Node returns Ignore for live admission for P-ECO-7 = 140 s (DEC-017). The simulator starts every Bus Node at once, which would stall each run for 140 s. The prototype therefore lifts the barrier early when the node started before the oldest eligible membership root was published: no Envelope can have been admitted under a root the node was already running for. Nodes that join later, including every churn rejoin, wait the full 140 s. This refinement is finding F2.

### 5.5 Peer scoring

Activated with `with_peer_score(params, thresholds)`. rust-libp2p's topic defaults enable P3 with threshold 20 and a 5 s activation (`peer_score/params.rs:316-318`), which drives every mesh peer of an idle Shard negative; MPE-NET-022 (corrected) forbids pruning in an idle Shard.

| Parameter | Value | Reason |
|---|---|---|
| thresholds gossip / publish / graylist | −10 / −50 / −80 | rust-libp2p defaults; with the P4 row below a peer with no positive score falls under them at 2, 3 and 3 invalid messages, a peer at the positive cap of 32 at 3, 3 and 4 |
| `accept_px_threshold` | 100 | reachable only through the bootstrapper application score (MPE-NET-027 shape) |
| `opportunistic_graft_threshold` | 5 | about 30 min of clean mesh time |
| `topic_score_cap` | 32 | bounds banked positive score, so an attacker cannot absorb many invalid messages after a long honest period |
| `app_specific_weight` | 1.0 | application scores: bootstrapper +200; listed relay 0; unlisted peer −20 while the allow-list is active (negative score refuses GRAFT, MPE-OPS-007, yet stays above graylist so its published messages are still validated); evicted peer −20 until its prune backoff ends |
| P1 `time_in_mesh` | weight 1/360 per s, quantum 1 s, cap 3,600 | at most +10 |
| P2 `first_message_deliveries` | weight 1.0, decay 0.99 per s, cap 20 | at most +20; rewards useful forwarders |
| P3, P3b | weight 0 | replaced by application eviction (below) |
| P4 `invalid_message_deliveries` | weight −10 (applied to the squared count), decay 0.99 per s (half-life 69 s) | 1 invalid: −10; 2: −40; 3: −90, graylisted (MPE-NET-021) |
| P6 IP colocation | weight −10, threshold 10 (P-NET-15) | MPE-NET-021; the simulator's TCP mode whitelists 127.0.0.1 and the P6 unit test uses 127.0.0.2 without a whitelist; memory transport carries no IP |
| P7 behaviour penalty | weight −10, threshold 6, decay 0.9 | broken IHAVE promises and GRAFT during backoff |
| `decay_interval`, `decay_to_zero`, `retain_score` | 1 s, 0.01, 3,600 s | a disconnect does not reset a bad score |

**Eviction (MPE-NET-022).** Per Shard the node counts loaded heartbeats: heartbeats in which it Accepted at least one Envelope on that Shard. A mesh peer that was the first deliverer of no Accepted Envelope, or delivered only Rejected ones, for 90 consecutive loaded heartbeats (P-NET-16) receives application score −20 and is pruned at the next heartbeat. rust-libp2p reports only first deliveries to the application, so "delivered within the mesh-delivery window" is approximated by "first deliverer at least once in 90 loaded heartbeats". At 10 Envelopes/s an honest mesh peer among 8 is first for roughly one Envelope in eight, so 900 Envelopes without a first delivery does not happen to a peer that forwards at normal speed. The application score is per peer, not per Shard; with one operating Shard this does not matter.

**Allow-list (DEC-006).** Default on: the mock Registry relay list defines the listed peers; unlisted gossip peers get −20. `--open` disables it for red-team runs (eclipse scenario). Removing a relay from the list sets its score to −20 at the next finalized Registry read, which prunes it within one heartbeat after that read (MPE-OPS-023 bound 600 s). Outbound mesh peers are dialled only from the relay list and bootstrappers (MPE-NET-028); the simulator has no DHT.

## 6. Admission stand-in

### 6.1 What it keeps from RLN

The stand-in implements the RLN-v2 relation of `2024-vac-rln-v2-spec` with SHA-256 and curve25519 scalar arithmetic in place of Poseidon over the proof field, and replaces the zero-knowledge proof by a value the Bus Node recomputes. Everything a relay checks is real: slot layout, epoch, root window, nullifier uniqueness, share binding to the EID, per-class limits from the leaf, equivocation evidence, and secret recovery from two shares.

| Value | Definition |
|---|---|
| admission secret `a0` | 32 B from the OS RNG, reduced to a curve25519 `Scalar`; independent of every other key (MPE-ECO-006) |
| identity commitment | `SHA-256("mpe/v1/idc" ‖ a0)` |
| leaf | `SHA-256("mpe/v1/leaf" ‖ idc ‖ u16 limits[0..4])`, limits (64, 16, 4, 1) for classes 0-3 (DEC-016) |
| root | RFC 6962 Merkle root over the leaves of one membership period |
| `a1` | `Scalar::from_bytes_mod_order_wide(SHA-512("mpe/v1/rln/a1" ‖ a0 ‖ epoch ‖ class ‖ credit index))` |
| nullifier | `SHA-256("mpe/v1/rln/nul" ‖ a1)` (MPE-ECO-017: secret, epoch, class, index, one domain) |
| `x` | `Scalar::from_bytes_mod_order_wide(SHA-512("mpe/v1/rln/x" ‖ EID))`; not transmitted |
| share `y` | `a0 + a1 · x`, 32 B little-endian scalar encoding |
| recovery | two shares under one nullifier: `a0 = (y1·x2 − y2·x1) / (x2 − x1)` (MPE-ECO-018) |

Scalar arithmetic comes from `curve25519-dalek` (already a dependency of `ed25519-dalek`; listed in COVERAGE.md as a direct dependency). No primitive is new.

### 6.2 Proof field and verification

- Proof (256 B) = `HKDF-Expand(PRK = HMAC-SHA-256(a0, "mpe/v1/standin"), info = epoch ‖ root ‖ nullifier ‖ y ‖ class ‖ EID ‖ N, 256)`.
- **Bus Node side.** The mock Registry gives Bus Nodes, and only Bus Nodes, a stand-in verifier table: for each member, its `a0`. At each epoch start a Bus Node precomputes `nullifier → (member, class, index)` for every member, class and index below twice the class limit (50 members: 8,500 hashes per epoch). Verification looks up the nullifier, recomputes `x`, `y` and the proof, compares in constant time, and returns `Valid`, `Invalid` (unknown nullifier, wrong share or proof; this also catches a different Network Identifier, MPE-FMT-021) or `OverQuota` (index at or above the class limit).
- **Cost model.** Verification busy-waits `--verify-cost-us` (default 4,500 µs, the Groth16 figure of `2024-revuelta-waku-latency` Table 1 used in RECONCILE) inside a blocking task, so queue bounds, fairness and CPU numbers mean something. If `nodes × offered rate × cost` exceeds half the host's cores, the simulator lowers the cost to fit and writes the value used into `notes` (at 200 nodes and 10/s on 6 cores: 1,500 µs).

### 6.3 What the stand-in does not have, and how a real proof replaces it

| Property | Stand-in | Real RLN |
|---|---|---|
| Unlinkability to Bus Nodes | none: a Bus Node maps every nullifier to a member | zero knowledge; Bus Nodes see only nullifier, share, root |
| Forgery resistance | members cannot forge for others; Bus Nodes can, because they hold `a0` | sound proof |
| Over-quota distinction | `OverQuota` separate from `Invalid` (for metrics) | both are a failed proof |
| Verification cost | synthetic busy-wait | measured (MPE-ECO-048, deferred) |

Replacement is one type implementing `AdmissionProof`: `prove` runs the circuit over the witness (`a0`, Merkle path, limits, credit index) with public inputs (epoch, root, nullifier, share, class, `x` from the EID), `verify` checks the proof against the verifying key, and the per-epoch table disappears. The slot layout leaves 152 B spare for a different encoding (A = 512 B holds 360 B of fields). Equivocation evidence, revocation and the restart barrier are unchanged. The stand-in's linkability is declared in the prototype's L-R leakage entry and must never appear in a privacy claim.

## 7. MockLedger and mock Indexer

### 7.1 Limits enforced

| Limit | Mock value | Midnight source |
|---|---|---|
| Block time | one block every 6,000 ms (real time) | `midnight-node/runtime/src/lib.rs:292` |
| Finality | a block is final 3 blocks after inclusion (18 s) | [doc] `midnight-improvement-proposals/mps/mps-0028-pre-finality-state-visibility.md:36-38` |
| Block usage | ≤ 1,000,000 B of transaction size per block; excess transactions wait for later blocks | `midnight-node/res/mainnet/ledger-parameters-config.json:158` |
| Bytes written | ≤ 50,000 B of Registry state writes per block | `ledger-parameters-config.json:159` |
| Transaction size | ≤ 1,048,576 B, else refused | `ledger-parameters-config.json:152` |
| Transaction size estimate | 8,192 B per transaction + 288 B per `Misc` event (**assumption**: DEC-PRF-6's 8 KiB transaction, used for Anchors in RECONCILE) | RECONCILE parameter table, Anchor row |
| Custom event | `Misc { name: Bytes<32>, payload: Bytes<256> }`, 288 B; the only custom event | `minokawa-compact/compiler/midnight-events.ss:71-74` |
| Log size | a log item over 1,024 B is silently dropped and counted in `events_dropped_over_limit` | ledger-9 `onchain-vm/src/vm.rs:41-43` (`MAX_LOG_EMITTED`, tag `ledger-9.1.0.0-rc.5`) |
| No signer | `MockTx` has no sender field; a fee is a public number with no payer link | `midnight-node/pallets/midnight/src/lib.rs:378, 450-468` |
| Pool longevity | a waiting transaction is dropped after 600 blocks | `pallets/midnight/src/lib.rs:592` |
| Intent TTL | ≤ 1,209,600 s | `ledger-parameters-config.json:176` |
| Phase | all parts of one ledger-carried Envelope in the guaranteed segment of one intent; a failing fallible segment discards its events | notes section 3.2; `mip-0019-multipart-event.md:64-78` |

### 7.2 Registry state (MPE-NET-039, MPE-NET-054, MPE-NET-055)

Shard count, activation height, maximum version, bootstrap-list hash, membership roots with period, publication and supersession times, the relay list (peer id, Operator organization id, roles relay/store/bootstrapper/gateway/anchorer), the bus pause flag, live Anchor records (at most 2,940, pruned past 176,400 s), the stand-in verifier table, and the `ledgerParameters` constants above. The Registry never stores an Event or Sealed Body (MPE-STO-001). A single maintainer key changes parameters (DEC-019 prototype default). Registration is a `MockTx` carrying a commitment and a simulated fee; the new root appears in the next block and is readable after finality.

### 7.3 Mock Indexer

`contract_events(contract, from_id, limit)` returns `Misc` events of one contract address from finalized blocks only, ascending monotonic id, inclusive cursor, at most `limit` (clamped 1-500, default 100), in drains of 20 rows (subscription batch size), matching `midnight-indexer/indexer-api/graphql/schema-v4.graphql:1971` and the limits in notes section 4.7. The contract address is required and is the only filter (MPE-CON-053). Delivery across calls is at-least-once; the client deduplicates by id. Retention coverage is reported as unknown.

### 7.4 Adapter failure modes

`--ledger freeze` stops block production; `--ledger skew:<s>` offsets the mock block time; `--ledger pause` sets the bus pause flag and makes user transactions fail. Under freeze the view becomes stale after 60 s: Bus Nodes keep Accepting Envelopes valid under cached roots (DEC-009), never Reject on chain- or clock-dependent checks, and Ignore Envelopes under roots older than the stale-root bound of 25 h (MPE-ECO-051). Clients keep delivering `gossip`-labelled Events and return `LedgerPaused` or `LedgerUnavailable` to reaction and fallback calls.

## 8. Store Node and back-fill

- **Admission to storage.** A Store Node stores what its own validator Accepts, keyed by `(expiry, EID)` in a per-Shard `BTreeMap` with a byte counter. The retention deadline is the visible `expiry` (RECONCILE row P-STO-1). Expiry beyond clock + 172,800 + 60 s refuses storage. The prototype store is in memory with a byte cap (`--store-cap`, default 256 MiB per Shard; production P-STO-3 is 32 GiB); restart durability is deferred (POC_CORE.md). Pruning removes records within 60 s of expiry.
- **Back-fill (MPE-PUB-030, MPE-PUB-031).** Request `{shard, from: Cursor, until}` where `Cursor = (expiry, EID)`, inclusive. Response: up to 64 Envelopes (P-PUB-9) in cursor order and a continuation cursor, or `head` when the newest held Envelope is reached. No Tag, topic or identifier list exists in the request. A Store Node that does not serve a request in full answers `Refused`, `ResourceExhausted` or `RetentionGap{from, to}`, never an empty page.
- **Portable cursor (MPE-PUB-043).** The cursor is made of header fields only, so it means the same at every Store Node. A client resumes from `(cursor.expiry − 60 s, zero)` and drops repeats by EID; the 60 s overlap covers Envelopes accepted out of expiry order.
- **Inventory (MPE-STO-041).** `{shard, window, after}` returns every retained EID in the window in pages of 64.
- **Receipts (MPE-STO-042, MPE-STO-012).** `{shard, window}` returns, for every retained EID in the window, an Ed25519 signature by the Operator key over `"mpe/v1/receipt" ‖ N ‖ EID ‖ shard ‖ deadline`. Receipts are requested per window for every identifier, never per recognized identifier, so the request carries no interest (MPE-PUB-012). A client marks an Event `stored` once receipts from 3 distinct Operator organizations (P-STO-5, MPE-OPS-055) name the same EID and deadline. At baseline this costs about 600 × 105 B per minute per Operator; the cost is reported.
- **Reconciliation (MPE-PUB-014, MPE-PUB-015).** Every 60 s the client fetches the inventory of `[last − 60 s, now − 5 s]` from a Store Node whose Operator differs from its feed source, compares it with every EID it received (matched or not; the client keeps all EIDs for 10 minutes), and back-fills each 60 s window that contains a missing EID from that second source. Fetching by window keeps MPE-PUB-030 intact and repairs every missing EID whatever the key set.
- **Historic roots (MPE-NET-056).** A Store Node validating a back-filled Envelope asks the Ledger Adapter for the referenced root with its period, published within the last 172,800 + 3,600 s, and consumes no new allowance.

## 9. Anchoring and the contract-consumer inclusion proof

- **Window assignment.** `window = floor((expiry − 172,800) / 60)`, the creation minute. Every node computes the same window from the header, independent of arrival time.
- **Batch roots (MPE-NET-051).** Per Shard, the RFC 6962 Merkle tree hash over the window's Accepted EIDs sorted ascending: leaf `SHA-256(0x00 ‖ EID)`, node `SHA-256(0x01 ‖ left ‖ right)`, empty tree `SHA-256("")`. Window root: the same construction over the per-Shard batch roots in Shard order.
- **Anchor (MPE-NET-050, DEC-024).** The anchorer waits 20 s after the window closes, then submits one `MockTx` that emits one `Misc { name: "mpe/anchor/v1" zero-padded, payload: window u64 ‖ window root ‖ u32 count per Shard }`: 44 B at 1 Shard, 72 B at 8. Empty windows produce no Anchor. The mock Registry keeps 2,940 live records and prunes records older than 49 h.
- **`final` label (MPE-CON-016).** A Subscriber recomputes the window's batch root from its own inventory. If the count and root equal the finalized Anchor, every Event of that window is `final`. If not, it fetches the anchorer's leaf list for the whole window and Shard (`/anchor-leaves`), verifies it against the Anchor, and labels the Events it holds that the list contains. No per-EID path is ever requested by a Subscriber.
- **Inclusion path (MPE-NET-052).** `/inclusion {eid}` returns `(window, shard, leaf index, path to the batch root, path from the batch root to the window root)`, about 10 × 32 B + 3 × 32 B at 600 leaves and 8 Shards. It refuses EIDs it did not anchor and serves paths for 49 h. Only a reacting consumer calls it, after deciding to disclose the Event to a contract.
- **Mock contract.** State: committed publisher keys, a nullifier set, an effect log. A reaction transaction carries the statement fields, the Ed25519 signature from the opened Envelope (in Midnight this would be private witness data), the consumption nullifier `SHA-256("mpe/v1/consume" ‖ N ‖ contract ‖ event secret)` (MPE-CRY-025), and optionally the inclusion proof with its window. The contract accepts only if the key is in its publisher set, destination and action match, expiry ≥ block time, the nullifier is new, and, when present, the path verifies under a live finalized Anchor. Nullifier insert and effect happen in one state transition; transactions apply sequentially within a block, so 100 racing reactors produce one effect (MPE-VER-032).

## 10. Ledger-only fallback

DEC-008: no ledger-only mode; the ledger carrier runs against the mock only, as a labelled last resort selected explicitly by the application (MPE-PRV-013).

- **Publish.** Class c ≤ 2 only: 4^c parts, at most P-FMT-8 = 16 (MPE-FMT-044). Class 3 returns an error before any transaction is built. The client builds one `MockTx` to the bus contract address whose guaranteed segment emits 4^c `Misc` events, each `name = "mpe/env/v1"` zero-padded to 32 B and `payload` = the next 256 B of the Sealed Body (MPE-FMT-040, MPE-FMT-041, MPE-FMT-043). No Admission Slot travels; the ledger fee is the rate limiter.
- **Read.** The client polls `contract_events(bus contract, from_id)` every 1 s (midnight-js `watchQuery` interval), groups parts by transaction and intent in emission order (MPE-FMT-045), discards groups whose count is not 1, 4 or 16 (MPE-FMT-046), runs the same Tag test and open on the reassembled body (MPE-FMT-037), rebuilds header bytes 0-7 from the `Misc` name, the part count, the audience key and the signed creation time, and delivers with carrier `ledger` and finality `final`.
- **Capacity under the limits.** Transaction size 8,192 + 288 × parts: class 0 = 8,480 B, class 1 = 9,344 B, class 2 = 12,800 B. One 1,000,000 B block holds 117, 107 or 78 of them: 19.5, 17.8 or 13.0 Events/s for the whole chain, about 2.0, 1.8 or 1.3 per second inside the 10% chain share of production (P-ECO-8). Latency is inclusion plus 18 s finality plus up to 1 s of polling.

## 11. Simulator design

### 11.1 Runtime

One tokio multi-thread runtime with one worker per core. Each Bus Node and each client is a `Swarm` driven by its own task; the MockLedger, MockIndexer and metrics registry are shared `Arc`s. Transport: `MemoryTransport` upgraded with Noise and Yamux, wrapped below the upgrade by a byte-counting `AsyncRead`/`AsyncWrite` adapter per node and direction, so counters include Noise, Yamux, GossipSub control and every MPE protocol (MPE-PRF-001 categories, MPE-PRF-005). `--transport tcp` runs the same harness on 127.0.0.1 with loopback whitelisted for P6. Proof verification runs in `spawn_blocking` behind a per-node semaphore of 1 and a global semaphore of `cores − 1`; per-peer queues are drained round-robin.

Topology at N Bus Nodes: 2 bootstrappers, 3 Store Nodes (one per Operator), 1 anchorer, the rest relays, all assigned round-robin to 3 Operator organization ids and listed in the mock relay list. Each Bus Node dials 10 random listed peers plus both bootstrappers. Clients: 10 publisher swarms hosting 4 memberships each (40 memberships) and 10 Subscriber swarms. A 10 s warm-up precedes the measurement window; the first membership root is in the MockLedger genesis block, which is final by definition and is created 1 s after every initial Bus Node has started; this lifts the restart barrier for the initial cohort (5.4) without waiting 18 s for finality.

### 11.2 Seeded workload

`ChaCha20Rng::seed_from_u64(seed)` derives node identity keys (so PeerIds repeat), memberships, 20 private streams, publisher-to-stream assignment (2 memberships per stream), Subscriber keys (4 streams each plus 28 decoy keys, 32 keys per Subscriber as in P-PRF-19), attacker placement and the publish schedule. The schedule is generated before the run: a Poisson process at 10 Envelopes/s on the one operating Shard, class drawn 60/25/10/5 by count (mean wire 2,158.4 B, 21.1 KiB/s, so the count cap binds), the publisher drawn among memberships with credit left in that class and epoch, payload length uniform in the class capacity. Each payload starts with a 16 B random canary. The schedule is deterministic; network timing is not, so repeated seeds give the same workload and slightly different measurements. `--load bytecap` publishes class 3 only at 3.88/s (65,536 B/s); `--load rate50` runs 50/s with the P-PRF-28 weights.

### 11.3 Run phases

Warm-up 10 s, publishing for `--duration-secs`, then a drain in which no new Event is published and delivery, repair and anchoring continue. Drains: 15 s (baseline, spam, malformed, replay, eclipse, leakage), 30 s (backfill), 40 s (fallback), 60 s (anchor), 125 s (churn: two reconciliation intervals plus 5 s). At 60 s the longest run is 195 s, inside the 5-minute limit. Latency counts from the publish call, so repairs during the drain show in the tail.

### 11.4 Metrics

| JSON key | How it is measured |
|---|---|
| `published` | Events the honest schedule submitted, each counted once regardless of retries. Replay scenario: replay injections. Fallback: see `fallback` |
| `delivered.expected` | eligible pairs: (Event, Subscriber holding that stream's key and present for the whole publish window; churn and backfill include Subscribers that join or move) |
| `delivered.received`, `ratio`, `per_subscriber_min_ratio` | pairs the Subscriber authenticated before the drain ended; ratio = received / expected; minimum over Subscribers of their own ratio |
| `latency_ms` | publish call to authentication at the Subscriber, same monotonic clock, over received pairs; missing pairs listed in `notes` with their count (MPE-PRF-003) |
| `duplicates` | deliveries to the application beyond the first per (Subscriber, EID) or (Subscriber, publisher, LEI); network duplicates are amplification, reported in `notes` |
| `rejected.*` | adversarial injections only, each counted once by the outcome at the first honest Bus Node that received it: `malformed` (steps 2-4, 6, 9 and unparseable), `oversize` (length above the class wire size; RPCs above 65,536 B are counted by the attacker harness as sent and verified undelivered), `bad_admission` (proof invalid, network mismatch, unknown root), `over_quota` (index at or above the limit, conflicting nullifier), `replay` (seen-set or same-EID nullifier hit), `expired` (step 8), `bad_signature` (valid admission, invalid sealed signature: counted when the first eligible Subscriber discards it) |
| `panics` | panic hook counter plus task `JoinError::is_panic` |
| `wire.envelope_sizes`, `distinct_sizes` | length histogram of every GossipSub message payload received by any Bus Node and every Envelope inside a client-protocol frame |
| `wire.plaintext_leaks` | captured frames containing any forbidden byte string (11.5) |
| `bandwidth.*` | counting-transport bytes per Bus Node over the publish window: p50 over Bus Nodes per direction, maximum per direction |
| `cpu_ms_per_node_p50` | per Bus Node: summed duration of every `poll` of its swarm task plus its blocking verification time; p50 over Bus Nodes |
| `store.max_bytes` | maximum over Store Nodes of retained Envelope bytes plus index entries at 72 B each |
| `store.backfill_expected`, `backfill_recovered` | backfill scenario: EIDs Accepted on the Shard before the late Subscriber joined; how many of them it obtained by back-fill |
| `anchor.batches` | Anchors final on the MockLedger |
| `anchor.inclusion_proofs_checked`, `valid` | every `final` determination by a Subscriber plus every inclusion proof a mock contract checked; the deliberately forged proofs of the unit tests are not counted here |
| `eclipse.*` | victim's attacker and honest peer counts at the end of warm-up; fraction of honest Envelopes the victim Accepted within 10 s |
| `spam.*` | attacker Envelopes submitted; distinct attacker EIDs Accepted by at least one honest Bus Node in phase A; quota = 64 × epochs spanned by phase A |
| `fallback.*` | Events submitted through the ledger carrier (class 3 refusals excluded, listed in notes); Events authenticated by Subscribers through the mock Indexer; sum of included transaction sizes; log items dropped by the 1 KiB rule or transactions dropped by pool longevity |
| `notes` | drain used, verification cost used, honest outcome counts per reason, variant results, mock limits hit |

### 11.5 Wire capture (leakage scenario)

Every Bus Node records every GossipSub message payload it receives (including those later Rejected or Ignored), and every client and Store Node protocol frame in both directions is recorded at the codec. This is the relay's view after Noise decryption; Noise ciphertext itself is not analysed. A scanner searches each captured frame for the forbidden strings the harness knows: every payload canary, Logical Event Identifier, stream secret, stream id, recognition key, encryption key, admission secret, identity commitment, publisher public key and schema id. `plaintext_leaks` is the number of frames with any match of 8 or more bytes. The same scanner runs over every log line the run wrote (MPE-VER-029). The scenario also runs the MPE-FMT-004 byte-distribution test (chi-square per offset outside `shard` and `expiry`, p > 0.01) on 1,000 Envelopes from one publisher and stream against 1,000 from distinct ones.

### 11.6 Scenarios

| Scenario | Set-up beyond baseline | Checked |
|---|---|---|
| `baseline` | 10/s, 1 Shard, 10 Subscribers | delivery ≥ 0.999, per Subscriber ≥ 0.99, p99 ≤ 10 s, no duplicates, ≤ 4 sizes |
| `spam` | one attacker membership. Phase A: 100 class-0 Envelopes/s through one ingress Bus Node: indices 0-63 valid, the rest over the limit or reusing an index with a new body. Phase B (notes only): the same membership injects conflicting Envelopes into 5 Bus Nodes at once | phase A accepted ≤ quota; phase B distinct EIDs accepted network-wide and delivered |
| `malformed` | 5 attacker gossip peers inject garbage, truncated, overlength, oversize-RPC, wrong-version, reserved, unknown-class, shard-mismatch, filler, corrupted-proof, wrong-network, far-future and expired Envelopes at 20/s each. Two attacker memberships add validly admitted Envelopes with a random Tag (Accepted by design, since validation is body-blind, and discarded by every Subscriber; counted in notes) and, from an insider holding one stream's secret but no authorized publisher key, Envelopes with an invalid sealed signature. Honest load continues | no panic; honest delivery ≥ 0.999 |
| `replay` | an attacker peer records 200 Envelopes Accepted in the first 2 s of publishing and re-injects the identical bytes from T0 + 62 s, past GossipSub's 60 s duplicate cache, so the application seen-set must catch them; its own membership re-admits 50 already-published bodies under new credit indices (same EID, new wire bytes); it injects 200 pre-built Envelopes whose expiry is 61 s in the past. `published` counts these 450 injections. Corrupted-slot copies sent ahead of honest Envelopes (MPE-SEC-042) are reported in notes, not counted | every injection Ignored as duplicate or expired |
| `eclipse` | `--open`; 20% of N are withholding attackers that dial the victim, accept GRAFT, never forward, and send IHAVE without answering IWANT; variant `poisoned` (notes) gives the victim a dial list that is 80% attackers | victim delivery ≥ 0.99 |
| `churn` | every 10 s, 10% of relays leave; the same number of fresh relays join, are listed, and wait out the restart barrier; Subscribers on a departed Bus Node fail over | delivery ≥ 0.99 after the drain |
| `backfill` | an 11th Subscriber joins at T/2 and back-fills from T0 from one Store Node; that Store Node is stopped at 0.75 T and back-fill completes from another Operator's Store Node | recovered = expected |
| `anchor` | anchorer active; 2 Subscribers verify `final`; one consumer reacts with an inclusion proof; 100 reactors race on one Event (notes) | ≥ 1 batch; every checked proof valid |
| `leakage` | baseline plus capture and scanner | 0 leaks, ≤ 4 sizes |
| `fallback` | overlay off for 3 fallback Subscribers that opted in; publishers use the ledger carrier at 2 Events/s, classes 0-2, plus a burst of 200 at T0 + 20 s, plus class-3 attempts | delivered = published; nothing dropped over a limit |

### 11.7 Optional flags

The fixed command line of the build brief is unchanged; these flags only add variants for `design/prototype/LEARNING_QUESTIONS.md`.

| Flag | Values (default first) | Purpose |
|---|---|---|
| `--mesh` | `8,6,12,4`, `6,5,12,2` | DEC-012 comparison (MPE-PRF-010) |
| `--idontwant` | `on`, `off` | MPE-NET-047 |
| `--msgid` | `wire`, `eid` | reproduce the DEC-010 attack |
| `--recognition` | `tag`, `trial` | DEC-003 comparison |
| `--shards` | `1`, `8` | DEC-011 benchmark topology |
| `--load` | `nominal`, `bytecap`, `rate50` | DEC-005, DEC-027 |
| `--verify-cost-us` | `4500`, any | synthetic proof cost (6.2) |
| `--p3` | `off`, `default` | rust-libp2p topic-score defaults against application eviction |
| `--open` | off, on | allow-list off (red team, DEC-006) |
| `--eclipse-variant` | `inbound`, `poisoned` | eclipse placement |
| `--ledger` | `live`, `freeze`, `skew:<s>`, `pause` | Ledger Adapter failure modes (7.4) |
| `--transport` | `memory`, `tcp` | transport under test |

## 12. Milestones

| Milestone | Time | Content | Exit test |
|---|---|---|---|
| M0 Envelope | 0:00-0:20 | `wire`, `keys`, `seal`, `tag`, vectors, independent decoder | `cargo test -p mpe-core` passes the vector, padding, capacity, AAD-tamper, Tag-recognition and signature-field tests |
| M1 Admission and validator | 0:20-0:45 | stand-in RLN, slot, seen-set, nullifier cache, evidence, validator steps 1-18, restart barrier, stale view, mock clock | table-driven test: every mutation of a valid vector yields its listed outcome and the verifier counter stays 0 for every structural failure |
| M2 Bus Node | 0:45-1:10 | GossipSub config and scoring, Shard topics, publish/feed protocols, allow-list, eviction, verify scheduler | in-process 8-node test: 100 Envelopes reach every node; corrupted-slot copies get distinct ids; an unlisted peer's GRAFT is refused; a 30-peer node sends a fresh Envelope to at most 12 peers |
| M3 Client and store | 1:10-1:30 | Subscriber pipeline, dedup, gaps, labels, outcomes; store, back-fill, inventory, receipts, reconciliation | 16-node test: 5% omission at one source is repaired from the second Operator within 120 s; three receipts give `stored` |
| M4 Ledger | 1:30-1:45 | MockLedger, Registry, MockIndexer, anchorer, inclusion proofs, mock contract, ledger carrier | anchor round trip verifies; 100 racing reactions give one effect; classes 0-2 round-trip through `Misc` parts, class 3 refused |
| M5 Simulator | 1:45-2:00 | harness, ten scenarios, metrics, capture, MPE-VER-041 scripted run | all ten scenarios at 50 nodes write valid JSON and `python3 design/prototype/check_sim.py <dir>` passes |

Later milestones depend only on the exit tests of earlier ones. If time runs out, M5 runs the scenarios whose components exist and reports the others as missing rather than faking them.

## 13. Risks

| # | Risk | Effect | Mitigation in the prototype |
|---|---|---|---|
| R1 | 137 core requirements in two hours | partial coverage, false coverage claims | build order puts privacy-critical items first; COVERAGE.md marks untested items as not done |
| R2 | rust-libp2p topic-score defaults (P3) prune honest peers in idle Shards | mesh collapse in the 8-Shard topology | P3 off, application eviction (5.5); measured in the idle-Shard run |
| R3 | rust-libp2p hides duplicate deliveries from the application | eviction approximates "delivered within the window" | documented; findings feed MPE-NET-022 |
| R4 | One 6-core host for up to 200 swarms with synthetic verification | CPU saturation distorts latency | cost scaled and recorded; 200-node runs only for baseline and churn |
| R5 | Memory transport has no IP, no link latency, no bandwidth limit | P6 untested in scenarios; latencies optimistic against P-PRF-9's 100 ms reference | P6 unit test on TCP with distinct loopback addresses; latency gate is the 10 s post-admission bound, not the 3 s propagation target |
| R6 | Stand-in admission is linkable and forgeable by Bus Nodes | wrong conclusions about privacy if misread | declared in L-R; no privacy claim rests on the stand-in |
| R7 | Restart barrier plus churn | rejoining relays relay nothing for 140 s; churn delivery leans on fail-over and repair | measured; learning question on DEC-017 |
| R8 | Equivocation race across ingress nodes | over-quota Envelopes reach Subscribers despite per-node checks | phase B of the spam scenario measures it; gate uses phase A |
| R9 | Host disk at 98% | store files or logs fill the disk | in-memory store; logs at info level; results only as JSON |
| R10 | gossipsub 0.50 (build) and 0.51 (local source) differ | line citations drift | behaviour re-checked in the M2 test, not by citation |

**Requirement findings the prototype will test.**

- F1. MPE-CRY-004 (bytes 0-7 in AAD) conflicts with MPE-FMT-037 and MPE-FMT-051 on the ledger carrier; the prototype binds bytes 0-3 in AAD, binds `expiry` through the EID and the signed statement, and fixes `expiry = creation + 172,800`. A shorter lifetime needs a sealed `expiry` field.
- F2. MPE-STO-015 read literally stalls any fresh network for 140 s; the prototype exempts nodes that started before the oldest eligible root.
- F3. MPE-NET-022's "mesh-delivery window" is not observable through the rust-libp2p application API.
- F4. MPE-STO-042 and MPE-CON-016 leak recognition if receipts or inclusion paths are requested per recognized Event; the prototype requests by window for every Envelope.
- F5. MPE-PUB-015 ("fetch that Envelope") and MPE-PUB-030 (no identifier list) conflict; the prototype repairs by window.
- F6. MPE-NET-048 is met by a 1 s pull feed (MPE-PUB-013 cadence), which adds up to 1 s of latency.

## 14. What the prototype will not prove

- Unlinkability of publications to Bus Nodes and the cost of a real admission proof: the stand-in reveals the member to every Bus Node and its verification time is synthetic (MPE-ECO-048 stays open).
- Anything about Midnight's real ledger, Indexer, fees or DUST: limits are copied into a mock; ledger-9 availability on public networks is unknown; Compact circuit size and proving time for the contract consumer are not measured (DEC-022).
- Behaviour at wide-area latency, bandwidth limits, NAT, or 1,000 nodes; the 72 h soak; the 24 h comparison at 50/s.
- Resistance to a determined Sybil adversary under open admission in production, or closure of CVE-2022-47547 for the pinned GossipSub; the eclipse scenario measures one targeted configuration only.
- Any timing, volume, relationship or global-observer privacy, any source anonymity from the one-hop ingress, any forward secrecy or post-quantum property: none is claimed at launch (MPE-PRV-024, MPE-PRV-026, MPE-PRV-027).
- Restart durability of Store Nodes, durable receipts, or behaviour across real process crashes beyond the scripted client crash of MPE-VER-041.
- Mobile recognition and download costs on phone hardware; the desktop benchmark gives the per-operation numbers only.
