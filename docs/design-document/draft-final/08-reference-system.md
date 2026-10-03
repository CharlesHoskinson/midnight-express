# The reference system {#ch8}

The reference system is the version of Midnight Express that the proof of concept will implement and that the experiments of Chapter 9 will run against. The proof of concept is the next step and does not exist yet. It will be written in Rust on rust-libp2p 0.57 with the `libp2p-gossipsub` 0.50 crate, and its first milestone will deliver a deterministic simulator and a runnable harness. Throwaway exploratory runs helped shape the choices below. Where a choice was prompted only by those runs, the text states it as a hypothesis and names its test in Chapter 9 or Chapter 11. Where the reference system departs from the requirement set, the text says so.

The reference system carries Messages. A Message is an application message that a Publisher seals and delivers; it is not a contract event. On the wire it travels as an MPE Envelope of fixed size: an 8-byte clear header, an Admission Slot and an encrypted Sealed Body. "Event" and "private event" keep the Foundation's meanings throughout. An event is a contract event that a Compact circuit emits and a transaction records [@midnight-mip-0002]. A private event is a contract event with fields encrypted for chosen recipients and bound to the transaction by a commitment that the proof checks. MPS-0005 plans private events for its Part 2, and the text of that part is not yet published [@midnight-mps-0005]. Chapter 4 defines a Confidential Message and a carried event. A Confidential Message is a Message with four properties: content confidentiality, sealed labels, conditional interest privacy and no silent change of leakage. The reference system covers Confidential Messages only and carries no contract event.

In the proof of concept, everything a Bus Node or a Subscriber does with an Envelope will be real code running over real libp2p connections. The Admission Proof, the ledger, the Indexer and the contracts the harness calls will be stand-ins. A stand-in here is code with the interface of the real component that enforces the rules the experiments depend on, but lacks the real component's security, its cost, or both. Separately, a Compact version of the ledger interface was written as exploratory code, compiled and costed. It was not run on a network, the design does not depend on it being final, and the harness will not call it.

## Components

The proof of concept will be a Rust workspace of four crates:

- `mpe-core`: the wire format, sealing, the admission stand-in, the validator, the store, the Merkle trees, and the mock ledger and Indexer.
- `mpe-node`: the Bus Node, meaning the libp2p swarm, GossipSub configuration and scoring, and the request-response protocols.
- `mpe-client`: the Publisher, the Subscriber, reconciliation, the consumer adapters and the ledger-lane carrier.
- `mpe-sim`: the deterministic simulator and the harness that Chapter 9 describes.

Figure 8.1 shows the components.

{{fig:8-1}}

The figure rests on two ideas. GossipSub is a libp2p publish-subscribe protocol. Peers subscribed to the same GossipSub topic keep full-message links to a few of the others, called the mesh, and forward every new message over those links; peers outside the mesh get only short announcements. A Shard is one such GossipSub topic, so a Bus Node that joins a Shard receives every Envelope published on it. An Anchor is a single hash posted on the ledger that commits to the identifiers of every Envelope of one minute, so that a list of identifiers can later be checked against the chain.

Two paths run through the figure. On the main path, a Publisher seals a Message and hands it to one Bus Node. The Envelope travels through a GossipSub mesh to every Bus Node on its Shard, where Subscribers test every Envelope locally and open the ones meant for them. On the side path, an anchorer commits each minute's Envelopes to the Bus Registry on the ledger. A Publisher that opts in can also write the sealed body to the ledger directly on the ledger lane, and a Subscriber reads it back through the Indexer. The Indexer is used in the Foundation's sense: a service that reads chain data and serves it to wallets and DApps [@midnight-mps-0028]. Table 8.1 lists the roles.

| Component | Role in the reference system |
|---|---|
| Publisher | Seals a Message into a fixed-size MPE Envelope, attaches the Admission Proof, and submits it to one Bus Node. In the design the Admission Proof shows that the sender is a registered member within its quota without saying which member; the stand-in does not hide which. If no acceptance comes back within 5 s, it sends the identical bytes to another Bus Node, up to 3 in all. |
| Bus Node | A sidecar process beside, not inside, a Midnight node. Joins one GossipSub topic per Shard, runs the application validator on every Envelope before forwarding it, and serves a whole-Shard pull feed to Subscribers outside the mesh. |
| Store Node | A Bus Node with the store role. Keeps every Envelope it accepts until the Envelope's visible expiry. Answers back-fill, inventory and receipt requests. It stores no chain history. |
| Anchorer | A Bus Node with the anchorer role. Computes one Merkle root per 60 s window over all Shards and submits it to the Bus Registry as an Anchor. |
| Bootstrapper | A Bus Node that new peers dial first. The specification intends a bootstrapper with mesh degree 0 that offers peer exchange. In the proof of concept bootstrappers will also relay, and peer exchange will not be configured. |
| Subscriber | Receives the whole Shard, either inside a Bus Node's process or through the feed. Tests each Envelope's Recognition Tag against its keys, opens matches, deduplicates and labels them. |
| Consumer adapters | An agent callback, a wallet stub that collects deliveries, and a contract reaction constructor. |
| Mock ledger | A stand-in for Midnight: 6 s blocks, finality after 3 blocks, a block budget of 1,000,000 B and a transaction limit of 1,048,576 B, `Misc` events (the Compact event type with a 32-byte name and a 256-byte payload), the 1 KiB event rule and no transaction signer. It hosts the mock Bus Registry, the shared ledger-lane contract and a mock consuming contract. |
| Mock Indexer | A read path over finalized mock blocks, shaped like the Indexer's `contractEvents` query and filtered by contract address only. |

The Bus Registry is the on-ledger record of everything the overlay needs to agree on. It holds the Shard count, the membership roots with their periods and publication times, the relay list (peer key, Bus Operator organization, roles), a pause flag and the live Anchors. The relay list names the Bus Nodes allowed in a mesh. A Bus Operator is the organization that runs Bus Nodes and signs their receipts. A membership root is a Merkle root: one 32-byte hash that commits to the list of registered members, against which a Publisher later shows that it is one of them. Each 24-hour membership period has its own tree and root. The Bus Registry never holds a Message or a Sealed Body.

In the proof of concept the Bus Registry will live inside the mock ledger, and one maintainer key will change its parameters. The compiled Compact version replaces the maintainer key with a steward secret proved in circuit and adds a time-lock to parameter changes. It cannot record publication times, because a circuit can compare the block time but not read it. The requirement set allows bonds as Bus Registry contract balances, unrelated to the staking of NIGHT, Midnight's native token [@midnight-mip-0016]; neither version implements them.

Figure 8.2 shows the parts of an MPE Envelope and its four wire lengths.

{{fig:8-2}}

## The life of one Message

Figure 8.3 traces one Message from the Publisher to a contract that reacts to it.

{{fig:8-3}}

The Publisher picks the smallest size class that holds the payload and draws a fresh 16-byte salt and a 12-byte encryption nonce. This Envelope's encryption key and Recognition Tag are both derived from the salt. The Publisher then computes the Recognition Tag, a 16-byte value that only holders of the stream's key can recognize, signs a statement about the Message, and encrypts. The Envelope identifier (EID) comes next, computed over the header and the Sealed Body. Only after that does the Publisher fill the Admission Slot, the 512-byte field for admission data. The order is forced: the admission share, which ties that data to one Envelope, is a function of the EID. The finished Envelope goes to one Bus Node over the publish protocol.

The ingress Bus Node runs the full validator. On Accept it publishes the Envelope on the Shard's GossipSub topic and returns the EID to the client. That acknowledgment means only that this Bus Node completed application acceptance and recorded it. It does not prove that any mesh peer received the Envelope, and a failure to queue the Envelope for sending is reported separately.

Every other Bus Node receives the GossipSub message from its mesh and holds it until its own validator returns Accept, Reject or Ignore. Accept forwards the Envelope, Reject refuses it and penalizes the peer that forwarded it, and Ignore drops it quietly. Some transport work happens before the validator speaks. The router computes the message identifier, records it in its seen cache, may send IDONTWANT (a notice telling mesh peers not to send a copy it already has) and updates delivery bookkeeping. Validation must also finish while the message is still in the router's message cache (5 heartbeats in this configuration), because Accept cannot forward a message the cache no longer holds.

A Subscriber embedded in a Bus Node reads that Bus Node's accepted stream directly, and its deliveries carry the carrier attribute `overlay`. A remote Subscriber pulls the feed from one Bus Node every second, and its deliveries carry `gateway`. Either way the Subscriber sees every Envelope on the Shard and tests every one.

A Recognition Tag match makes the Envelope a candidate, nothing more. The Subscriber opens the authenticated encryption, which fails if any byte of the ciphertext or of the data bound to it was changed. It then checks the padding, verifies the Publisher's signature against the keys named in its invitation, compares the signed expiry with the visible one, and only then delivers. Every 60 s it compares the EIDs it has seen with the inventory of a Store Node run by a different Bus Operator and back-fills any window with a gap.

About 80 s after the Message's creation minute begins, the anchorer posts that minute's root, and 18 s later the Anchor is final. The Subscriber can then relabel the Message from `gossip` to `final`, which means "covered by a Bus Registry Anchor in a finalized block". Take a Message created at 12:00:30. Its creation minute ends at 12:01:00, and the anchorer posts at about 12:01:20. Three 6 s blocks later, at about 12:01:38, the Anchor is final: 68 s after creation (80 + 18 − 30).

On a real ledger the anchorer must also prove a k = 18 circuit for each Anchor. The number k gives the size of a circuit: its table has 2^k rows, the smallest power of two that holds the circuit's rows, here 2^18 = 262,144. Its proving time is unknown.

If the application wants a contract to act, it must construct a reaction transaction itself; nothing in the pipeline does so on its own.

## The MPE Envelope

An MPE Envelope passes through relays that check it but cannot read it. Its length is still visible. If Envelopes had the length of their payloads, a relay could tell a 40-byte acknowledgment from a 10 KB document without opening either.

### Size classes

Every MPE Envelope therefore has one of four wire lengths, and within a class the payload length is hidden. The class itself remains visible, and so do the rate and timing of Envelopes and the transport transcript around them: GossipSub framing, batching of several messages into one RPC, and control messages all vary. Table 8.2 gives the classes. The fixed overhead is the 8-byte visible header, the 512-byte Admission Slot and 170 bytes inside the Sealed Body, so payload capacity is the body length minus 170.

| Class | Sealed Body (B) | Wire length (B) | Payload capacity (B) | Envelopes per second at 64 KiB/s | Ledger `Misc` parts |
|---|---:|---:|---:|---:|---:|
| 0 | 256 | 776 | 86 | 84.5, capped at 10 | 1 |
| 1 | 1,024 | 1,544 | 854 | 42.4, capped at 10 | 4 |
| 2 | 4,096 | 4,616 | 3,926 | 14.2, capped at 10 | 16 |
| 3 | 16,384 | 16,904 | 16,214 | 3.88 | 64 |

The per-second figures are derived: 65,536 B divided by the wire length, then capped at the Shard's 10 Envelopes per second. Only class 3 reaches the byte budget before the count cap. A payload over 16,214 B returns `TooLarge` before any admission work, and the largest Envelope, plus its protobuf framing, is far below the 65,536 B frame limit configured for GossipSub.

Class 0 spends 690 bytes of overhead (8 + 512 + 170) to carry 86 bytes of payload. Part of the overhead is a constant-size slot sized for a zero-knowledge proof not yet selected; the rest is a sealed header that carries a signature. Chapter 7 gives the reasoning behind the slot width.

### Byte layout

The fenced block gives the offsets of the parts shown in Figure 8.2. All integers are big-endian, and offsets count from the first wire byte. `B` is the Sealed Body length of the class.

```
offset  length   field
------  -------  -----------------------------------------------
     0        1  version            = 1
     1        1  size_class         0 to 3
     2        1  shard              equals the GossipSub topic's Shard index
     3        1  reserved           = 0
     4        4  expiry             u32 Unix seconds
---- Admission Slot (512 B) ------------------------------------
     8        8  admission window   floor(unix / 60)
    16       32  membership root
    48       32  admission nullifier
    80       32  share y
   112      256  proof
   368      152  zero fill          any non-zero byte: Reject
---- Sealed Body (B bytes) -------------------------------------
   520       16  salt
   536       12  AEAD nonce
   548       16  Recognition Tag
   564   B - 44  ChaCha20-Poly1305 ciphertext, 16 B authenticator last
```

The ciphertext covers a plaintext of `B − 60` bytes whose first 110 bytes form a sealed header:

```
offset  length   field (inside the plaintext)
------  -------  -----------------------------------------------
     0        1  pt_version         = 1
     1        1  kind               1 = application Message
     2        2  flags              bit 0 = authentication block present
     4        2  payload_len
     6        2  schema_version
     8        8  seq                per Publisher and stream, +1 per Message
    16       16  Logical Message Identifier (random, same on every retry)
    32        8  schema id
    40        2  authorized-key index into the invitation's key list
    42        4  creation time      u32 Unix seconds
    46       64  Ed25519 signature
   110  payload  payload
   rest          zero padding       any non-zero byte: discard
```

The two blocks fit together by subtraction. The salt, nonce and Recognition Tag take 16 + 12 + 16 = 44 bytes and the authenticator 16 more, so the plaintext is B − 60 bytes. The 110-byte sealed header leaves B − 170 for payload and padding: 86 bytes in class 0.

A relay sees the first eight bytes, the Admission Slot, the salt, the nonce and the Recognition Tag. The version, class and reserved byte are the same for every Envelope of a class. The Shard is a function of the stream secret, so it partitions streams but cannot tell two streams on one Shard apart. The expiry is creation time plus 48 hours, which leaks the creation second; Chapter 4 counts this among the timing leaks the design does not claim to hide. Everything an application would recognize (stream, Publisher, sequence number, schema, Logical Message Identifier) is inside the ciphertext.

The reference system specifies only kind 1. The requirement set reserves a schema identifier for a carried event, whose payload is the unchanged `VersionedLogItem` bytes of a contract event with the transaction hash and the event's position in it. A Consumer decodes such a payload only with the Foundation's own decoder for its event type and version. It treats the payload as `gossip` until the transaction is finalized and the bytes match its transcript, the public record of the ledger operations a contract call performs. A single contract event is at most 1 KiB serialized, so a carried event fits class 1 only if it and its transaction reference stay within 854 bytes; larger ones need class 2. None of this is in the proof of concept, and carrying a private event in the Foundation's sense also depends on MPS-0005 Part 2, which is not published.

### Keys and sealing

The reference system specifies one profile, `mpe-v1-sym`, which uses HKDF-SHA-256, HMAC-SHA-256, ChaCha20-Poly1305 and Ed25519; the proof of concept will take them from standard Rust crates. HKDF turns one secret into several independent keys by mixing in a different label for each, and HMAC is a keyed hash that only a holder of the key can compute. A private stream is defined by a 32-byte stream secret `S`, drawn from the operating system's generator. The stream's members receive it out of band in an invitation, together with the Publishers' public keys. `N` is the 32-byte network identifier: the Midnight genesis hash in production and a fixed constant in the mock. Table 8.3 lists the values derived from them.

| Value | Derivation |
|---|---|
| Recognition key | HKDF-SHA-256 with salt `N`, input `S`, info `"mpe/v1/rec" || profile` (32 B) |
| Recognition Tag | first 16 bytes of HMAC-SHA-256(recognition key, `"mpe/v1/tag" || N || salt`) |
| Encryption key | HKDF-SHA-256 with the Envelope's salt, input `S`, info `"mpe/v1/enc" || N || profile`; one key per Envelope |
| Stream identifier | SHA-256(`"mpe/v1/stream" || S`); inside the ciphertext and the signed statement only |
| Shard | first 8 bytes of SHA-256(`"mpe/v1/shard" || S`) as an integer, modulo the Shard count |
| Message secret | HKDF-SHA-256 with salt `N`, input `S`, info `"mpe/v1/event" || Logical Message Identifier` |
| EID | SHA-256(`"midnight-pe/id/v1" || N || wire bytes 0 to 7 || Sealed Body`) |
| GossipSub message identifier | SHA-256(`"mpe/v1/msgid" || complete MPE Envelope`) |

The per-Envelope key removes a known hazard. If one ChaCha20-Poly1305 key encrypts two plaintexts under one nonce, an observer can combine the ciphertexts to learn about both and can forge new ones. Each Envelope's 16-byte salt is fresh, so each encryption key encrypts exactly one plaintext, and nonce reuse under one key would need a salt collision, about 2^-128 per pair. A retransmission sends the stored bytes and never re-encrypts, so restoring client state from a backup cannot cause reuse either. No counter is involved.

The associated data of the encryption is `"mpe/v1/aad" || N || wire bytes 0 to 3 || salt || nonce || Recognition Tag`. Associated data is authenticated without being encrypted, so a change to any byte of it makes the open fail. The Publisher signs a 244-byte statement with the following fields:

- a domain string and `N`;
- a hash of the first four header bytes and the clear prefix (the salt, nonce and Recognition Tag that open the Sealed Body);
- the stream identifier, the Logical Message Identifier and the sequence number;
- the schema identifier and version;
- the creation and expiry times;
- a hash of the payload;
- a destination contract and action, both zero when unused.

A contract later checks this statement. It names the Message without carrying its body or any stream key.

The domain labels in Table 8.3 are those of the reference system. Midnight has no shared convention for domain-separation tags yet [@midnight-mps-0027], so the requirement set moves every label to one scheme and publishes the label table for registration once a registry exists. It also adds a one-byte suite identifier inside the profile binding, following the suite byte of MIP-0012's `InboxEntry` [@midnight-mip-0012], so that suites can be added without a version change. A profile that encrypts to a recipient's Midnight shielded encryption key is deferred until MPS-0005 specifies `encrypt_for` [@midnight-mps-0005]. The reference system has no suite byte; the profile name in the key derivation plays that role.

### Visible-header binding

The associated data covers bytes 0 to 3, not bytes 0 to 7. This departs from the requirement as written (`MPE-CRY-004` binds the whole header), and the departure is deliberate. The ledger lane transmits only the Sealed Body, so a ledger reader cannot know `expiry` before it decrypts, and yet the ledger copy must open exactly like the overlay copy (`MPE-FMT-037`). Bytes 0 to 3 can be reconstructed on either carrier: the version from the `Misc` event name, the class from the part count, the Shard from the stream secret and the reserved byte as zero.

The expiry stays bound twice. The EID covers bytes 0 to 7 and the admission share depends on the EID. In the design, a relay that changes `expiry` by even one second therefore moves the point at which the share must lie, and every honest Bus Node rejects the copy at proof verification (step 17 of Table 8.4). The stand-in weakens this, because a Bus Node holds every `a0` and can recompute the share and the proof; there only the second binding catches the change. The signed statement also carries `expiry`, and the Subscriber rejects an Envelope whose visible expiry differs from creation time plus 172,800 s (48 × 3,600).

The cost is that every Message has the same 48-hour lifetime. A shorter lifetime would need a sealed expiry field of 4 bytes, reducing every class's capacity by 4. The decision register records this as a change to the requirement set.

### Recognition Tags and recognition

A Subscriber holds one recognition key per stream it follows, up to 256. For each Envelope on its Shard it computes one HMAC per key over the network identifier and the Envelope's salt and compares the first 16 bytes with the Recognition Tag in constant time. On a match it tries to open the Envelope; either way it sends nothing. A chance match has probability 2^-128 per key and Envelope. Because the salt is fresh, two Envelopes from the same stream carry unrelated Recognition Tags, and a relay cannot group them by Recognition Tag. It can still group them through the Shard, the ingress connection, the admission data, timing and outside observations, and the admission stand-in described below links every Envelope to its member outright.

What this hides is conditional. Every Subscriber downloads and tests the whole Shard, so the Shards it receives, its online schedule and its traffic do not depend on which Envelopes it recognizes. That holds only while recognition changes nothing the Subscriber sends: no subscription, request, acknowledgment, retry, error, repair request, receipt request or diagnostic may depend on a match. The Shard membership itself is visible, because GossipSub announces subscriptions to connected peers, and so are participation and traffic. GossipSub provides no proof of this property. It rests on client behaviour, and Chapter 9 specifies a comparison of paired transcripts to test it.

The Recognition Tag serves the purpose that MPS-0005 gives topic-based filtering, which spares a recipient from trying to decrypt everything [@midnight-mps-0005]. The mechanism differs. The Foundation's planned filter runs at the Indexer per wallet, whereas a Recognition Tag is per Envelope, unlinkable without the key, and evaluated only by the Subscriber. An Indexer-side filter of that kind would be a reduced-privacy selective profile in the terms of the requirement set, not the default.

The recognition work can be counted from the derivation. The tag input is 58 bytes (the 10-byte label `"mpe/v1/tag"`, the 32-byte `N` and the 16-byte salt). With the key's inner and outer pad states precomputed, one HMAC-SHA-256 evaluation takes three SHA-256 compressions: two for the inner hash (64 + 58 + 9 = 131 bytes of padded input, three blocks, one of them precomputed) and one for the outer (64 + 32 + 9 = 105 bytes, two blocks, one precomputed). At the 256-key limit and 10 Envelopes per second that is 2,560 evaluations and 7,680 compressions per second. The time this takes on the hardware classes of the requirement set is for the proof of concept to measure (Chapter 11, experiment 2). The download is the larger cost. A whole Shard at its byte cap is at most 65,536 B × 86,400 s, about 5.66 GB per day. At the count cap with only class 0 it is 776 B × 10 × 86,400, about 0.67 GB per day. Both figures exclude GossipSub framing and duplicate copies.

The salted Recognition Tag works only between parties who already share a stream secret. First contact uses authenticated invitations only (`DEC-020`), and fuzzy detection clues [@2023-pu-fuzzystealthsigs] are not part of the design. Salted Recognition Tags have not been compared with trial decryption under every key, so the recognition decision (`DEC-003`) stays open until Chapter 11's experiment 2 is run.

## Admission

The overlay has to refuse spam without learning who published. A Bus Node that knew each Publisher's identity could count its Envelopes, but the design keeps that identity from relays.

### What a relay checks

Midnight Express uses a rate-limiting nullifier (RLN) proof in the style of Waku RLN Relay [@2021-vac-waku2-rln-relay-spec; @2022-taheri-waku-rln-relay]. It uses the version 2 form, which gives each member a message budget per admission window rather than one message per window [@2024-vac-rln-v2-spec]. A zero-knowledge proof convinces a verifier that a statement about secret data holds and reveals nothing else about the data. Here the statement has three parts: the sender is a registered member, its credit index is within its limit, and the admission nullifier and share were computed from its secret. An admission nullifier is a value that only the member can compute. It comes out the same whenever the same credit is spent twice, so reuse is visible without the admission nullifier naming the member.

A member registers a commitment to a secret `a0` and a set of per-class limits, and the Bus Registry publishes a Merkle root over the members of each membership period. To publish, the member picks an unused credit index `i` for the Envelope's class in the current 60-second admission window and computes:

- `a1` = a hash of (`a0`, admission window, class, `i`) reduced to a curve25519 scalar;
- admission nullifier = SHA-256(`"mpe/v1/rln/nul"` || `a1`);
- `x` = a hash of the EID reduced to a scalar (not transmitted; every Bus Node recomputes it);
- share `y` = `a0 + a1 · x`.

This is the RLN-v2 relation with SHA-256 and curve25519 scalars in place of Poseidon hashing over a proof field [@2024-vac-rln-v2-spec]. One credit index used for two different Envelopes yields one admission nullifier with two points on the same line, and anyone holding both can solve for `a0`: `a0 = (y1·x2 − y2·x1) / (x2 − x1)`. The per-class limits are 64, 16, 4 and 1 Envelopes per admission window. The admission nullifier changes with every index and window, so the slot carries no value that stays constant for one Publisher.

The line explains both halves of the guarantee. One point on a line of unknown slope says nothing about where it crosses the axis, so one honest Envelope reveals nothing about `a0`; two points fix the line. With small integers in place of scalars, take `a0 = 5` and `a1 = 3`. An Envelope with `x1 = 2` carries `y1 = 11`, and a second under the same credit with `x2 = 4` carries `y2 = 17`. Then `a0 = (11·4 − 17·2) / (4 − 2) = 5`, and the member's secret is public.

### The stand-in proof

The proof field in the proof of concept will not be a zero-knowledge proof. In the stand-in, the 256-byte proof is an HKDF expansion keyed by `a0` over the public inputs, and the mock Bus Registry gives every Bus Node a table of every member's `a0`. At each admission window a Bus Node precomputes the admission nullifier for every member, class and index below twice the class limit. To verify, it looks the admission nullifier up, recomputes the share and the proof, and compares in constant time. The verdict is `Valid`, `Invalid`, or `OverQuota` when the index is at or above the limit. A real proof would fold the last two into one failure; the stand-in separates them so the experiments can count over-quota attempts. The checks a relay makes around the proof will be real:

- the slot layout;
- the admission-window check and the root window;
- admission-nullifier uniqueness;
- the binding of the share to the EID;
- the per-class limit;
- the recovery of a secret from two shares.

Three consequences follow, and none of them may be read as a property of the design. Every Bus Node can map every Envelope to its member, so publications are linkable to members by every relay. Members cannot forge admission for each other, but Bus Nodes can forge for anyone, because they hold the secrets. And the verification time is synthetic: each verification will busy-wait 4.5 ms in a blocking task, the verification time Revuelta and colleagues report for one of their benchmark platforms [@2024-revuelta-waku-latency, Table 1]. The delay gives the queue bounds and CPU figures a cost to act on. It is not a measurement of any proof system.

Replacing the stand-in means one new type behind the `AdmissionProof` interface. Its prover runs a circuit over the member's secret, Merkle path, limits and credit index, and its verifier checks a proof against a verifying key. The per-window table disappears. The slot layout uses 360 of its 512 bytes (8 + 32 + 32 + 32 + 256), leaving 152 bytes for a different proof encoding. Evidence handling, revocation and the restart barrier do not change.

Two constraints from the Midnight side bear on the choice. First, a proof in Midnight's own proof system is 2,800 to 4,368 bytes in the compiler's circuit model for the ledger interface contracts. It does not fit the slot and would need a wider slot and new size classes. Second, a prover that runs on a remote server receives the private witness [@midnight-mps-0004]. The admission secret must therefore never go to a prover outside the client's trust boundary unless that prover is attested. The selected proof system must also run locally on the hardware classes of the requirement set, and whether any candidate does is unknown.

The compiled Bus Registry's revocation circuit checks the RLN relation in Compact, with the native field and `transientHash` (Poseidon), as an in-circuit admission proof on Midnight would. Compact does not guarantee that `transientHash` stays stable across upgrades, so the admission relation needs a hash that Midnight commits to keeping. Which hash that is remains open.

### The validator

Every Envelope, whether it arrives from the mesh or from a client, goes through the same validator. The order puts every check that needs no state and no cryptography first, so that malformed traffic never reaches proof verification. A Reject means the Envelope is invalid whatever the chain says. It suppresses delivery and forwarding, and it applies the P4 invalid-delivery penalty, a GossipSub score penalty for invalid messages, to the forwarding peer and to tracked duplicate forwarders. That peer is the one that handed the Envelope on, not necessarily whoever created it, so an honest relay can be penalized for forwarding traffic it could not judge. An Ignore means "not now, or not from me". It suppresses delivery and forwarding without P4 and earns no delivery reward, but it does not rule out every other score or resource effect.

The split between them follows from who would be blamed. An Envelope whose class byte says 0 but which is 1,544 bytes long is wrong at every Bus Node, so blaming the forwarder is fair. An Envelope under a membership root this Bus Node has not yet seen may be valid a block later, and blaming the forwarder for it would punish an honest peer for a local delay. Table 8.4 gives the order as specified.

| Step | Check | Outcome on failure |
|---|---|---|
| 1 | At most 20 Envelopes per second per peer per Shard (token bucket) | Ignore |
| 2 | Length at least 8 | Reject |
| 3 | Version equals the GossipSub topic's | Reject |
| 4 | Reserved byte zero | Reject |
| 5 | Class at most 3 | Reject |
| 6 | Length equals 520 + B | Reject |
| 7 | Shard equals the GossipSub topic's | Reject |
| 8 | Expiry no later than clock + 172,800 s + 60 s | Reject; Ignore if the chain view is stale |
| 9 | Expiry no earlier than clock − 60 s | Ignore |
| 10 | Slot filler bytes zero | Reject |
| 11 | EID already accepted | Ignore |
| 12 | Restart barrier active | Ignore |
| 13 | Clock inside the admission window, with 20 s of tolerance either side | Ignore |
| 14 | Root current, or superseded less than an hour ago, and its period began less than 25 hours ago | Ignore |
| 15 | Admission nullifier already seen with the same EID | Ignore |
| 16 | Fewer than 8 queued jobs for this peer and 128 for the Bus Node | Ignore; `Busy` to a publishing client |
| 17 | Proof verification, drawn round-robin across peer queues | Reject |
| 18 | Admission nullifier seen with a different EID and the proof valid | Ignore; keep both Envelopes as evidence |
| 19 | Insert EID and admission nullifier; hand to store and anchorer | Accept |

No step reads the Sealed Body beyond hashing it. A Recognition Tag that matches no one, or a Sealed Body whose signature fails, gets through the validator, and Subscribers discard such Envelopes when they open them. The version check in step 3 applies only to GossipSub topics the Bus Node supports. A Bus Node never subscribes to a GossipSub topic whose version it does not understand, so a valid Envelope from a future profile is never penalized. The EID enters the accepted set only at step 19. Inserting it earlier would let a copy with a broken slot block the honest copy.

The chain view counts as stale when the local clock and the latest finalized block time differ by more than 60 s. While it is stale, any Reject that depends on the clock or the chain becomes an Ignore, so a Bus Node with a lagging view never penalizes honest peers.

The accepted set keeps an EID until its expiry plus 60 s. At 10 Envelopes per second that is about 1.73 million identifiers per Shard (derived: 10 × 172,860). This state is separate from GossipSub's seen cache, and a Bus Node that cannot keep it refuses new admissions rather than evicting unexpired entries. The admission-nullifier cache keeps entries for 140 s.

Step 18 handles equivocation: two Envelopes under one credit. The second is verified before it is recorded, so in the design a forged slot cannot plant evidence against an honest member. Under the stand-in it can, since a Bus Node holds every member's secret and can forge a second Envelope under an honest member's credit, which step 18 would keep as evidence. Each Bus Node enforces this only against what it has itself seen. A member who sends conflicting Envelopes to different ingress Bus Nodes at the same moment gets each accepted somewhere. The quota holds per Bus Node, not across the network. Mesh connectivity does not change that, and the retained evidence makes the cheating detectable after the fact. Chapter 9 measures how many conflicting Envelopes reach Subscribers before the evidence spreads (Q9).

### Restart barrier and the Busy reply

A Bus Node that restarts has lost its admission-nullifier cache, so it cannot tell whether a credit was already used. For 140 s after every start it Ignores live admissions: two 60 s admission windows plus the 20 s tolerance, after which every admission nullifier it could have missed has expired. A fresh network would stall for 140 s under this rule. The reference system therefore exempts a Bus Node that started before the oldest eligible membership root was published, since nothing can have been admitted under that root before the Bus Node was running. Every Bus Node that joins later waits the full 140 s. The barrier and the exemption are application invariants. GossipSub gives no help in recovering allowance state, and clock errors or concurrent verifications can still break the invariants.

During the barrier the proof of concept will not stay silent towards a publishing client. Here it departs from the requirement set, under which the Bus Node returns nothing (`MPE-NET-049`). When the validator Ignores for the barrier, a full queue, the rate limit or a stale view, the publish protocol will answer `Busy`; for any other refusal it will answer `Refused`. These are replies of the publish service, not GossipSub validation outcomes. The client then moves on to another Bus Node at once, instead of waiting out its 5 s retry timer. The exploratory runs prompted this reply, so whether it improves delivery during the barrier is a hypothesis. Chapter 9 tests it under Q8 by running the reply and silent Ignore as paired variants under churn. The reply is confirmed if delivery reaches at least 0.999 after the drain with repair carrying less than 2% of pairs.

## GossipSub v1.2 configuration

Bus Nodes speak version 1.2 of GossipSub, which is v1.1 with its peer scoring [@2020-gossipsub-v11-spec; @2020-vyzovitis-gossipsub] plus the IDONTWANT control message. Without IDONTWANT, several of a Bus Node's eight mesh peers can send it the same 16,904-byte class-3 Envelope at nearly the same moment. The v1.2 specification has not reached final status.^[libp2p/specs, pubsub/gossipsub/gossipsub-v1.2.md; Working Draft r2, 30 August 2026, accessed 1 October 2026.] A v1.1 peer can still talk to a v1.2 peer, but that link carries no IDONTWANT. Midnight Express therefore requires v1.2 behaviour: the v1.1 scoring and mesh rules plus IDONTWANT.

### Shard names and protocol identifiers

When two libp2p peers open a stream, they agree on a protocol identifier, a string that selects the protocol and its version. A GossipSub topic is a name used inside that protocol. Each Shard is one GossipSub topic named `/mpe/<g>/1/shard/<i>`, where `<g>` is the first 8 bytes of the network identifier in lowercase hexadecimal and `1` is the Envelope version. Putting version and network into the name keeps the subscriptions of different networks apart and makes a version change a GossipSub topic change.

The names are routing labels, not authenticated network identifiers. Admission binds the full genesis hash, and a 64-bit prefix does not guarantee collision-free separation. The names also show anyone connected the network prefix, the major version and which Shards a peer joins. The proof of concept will run one Shard, and the benchmark topology of Chapter 9 uses eight. The request-response protocols use the same prefix: `/publish`, `/feed`, `/backfill`, `/inventory`, `/receipts`, `/anchor-leaves` and `/inclusion`, each with a length-prefixed CBOR codec. Connections use TCP, Noise and Yamux: Noise authenticates and encrypts each connection, and Yamux carries many streams over it.

The specification requires a Bus Node to accept subscriptions only to supported versions, the selected network prefix and the Shards that the Bus Registry authorizes. The proof of concept will use the crate's default subscription filter, which caps the number of subscriptions but allows any name, so it will not enforce the rule. Partial-message extensions and other extensions that change GossipSub's behaviour are outside the launch profile.

The transport profile requires negotiating the standard identifier `/meshsub/1.2.0`, and accepting a library's default offer does not meet that requirement. The inspected Rust and Go libraries also offer v1.3 and older versions, and a successful negotiation can select one of them. A Bus Node must record the identifier and peer kind it negotiated and enforce the version policy.

The stock rust-libp2p crate cannot pin v1.2 under a custom protocol identifier. Its `protocol_id` configuration method takes a `Version` argument that accepts only `V1_0` or `V1_1`, and that argument, not the string, selects the internal behaviour.^[libp2p/rust-libp2p, protocols/gossipsub/src/config.rs, enum `Version` and `ConfigBuilder::protocol_id`; libp2p-gossipsub 0.50.0 and 0.51.0 source, accessed 1 October 2026.] A custom name ending in `1.2.0` with `V1_1` therefore runs v1.1 with IDONTWANT off. The proof of concept will carry a small patch to a vendored copy of the 0.50 crate that adds a `V1_2` arm, and will negotiate `/mpe/<g>/1/gossipsub/1.2.0`. That identifier does not interoperate with peers that speak only the standard identifiers unless they are configured for it. Whether the change will be accepted upstream is unknown.

### Router settings

The mesh degree D is the number of mesh peers a router aims for on each GossipSub topic. The router adds peers with GRAFT below D_low, drops them with PRUNE above D_high, and keeps at least D_out on connections it dialled itself. At each heartbeat, its periodic maintenance tick, it repairs the mesh and sends gossip to peers outside the mesh: an IHAVE lists recent message identifiers, and the receiver asks for those it lacks with IWANT. The gossip factor sets the share of non-mesh peers that receive IHAVE, subject to a minimum count. The prune backoff is how long a pruned peer must wait before grafting again. Table 8.5 gives the router settings and the reason for each.

| Setting | Value | Why |
|---|---|---|
| Message authenticity and validation mode | StrictNoSign: published with no author, sequence number, signature or key; incoming messages carrying them are invalid | Under StrictSign, the Bus Node that first publishes a GossipSub message stamps it as author, and every relay preserves that stamp. Admission, not authorship, is what the overlay checks. |
| Application validation | On; the payload is forwarded only after the validator reports Accept | Invalid Envelopes must stop at the first honest hop. |
| Message identifier | SHA-256 over a domain string and the complete MPE Envelope | See below. |
| Mesh degree D, D_low, D_high, D_out | 8, 6, 12, 4 (crate defaults 6, 5, 12, 2) | A larger mesh and more outbound links resist mesh capture through inbound connections during a cold start [@2020-vyzovitis-gossipsub]. |
| Heartbeat, gossip factor, prune backoff | 1 s, 0.25, 60 s | The heartbeat and backoff [@2020-vyzovitis-gossipsub] used in the parameter set. |
| Flood publishing | Off (on by default in the v1.1 specification [@2020-gossipsub-v11-spec] and in the crate) | Reduces the first burst of copies and the ingress Bus Node's egress. |
| Maximum transmit size | 65,536 B | The encoded RPC frame limit. |
| Duplicate cache | 60 s (Rust crate default; Go's default is 120 s) | The application's accepted set covers the rest of the 48-hour lifetime. |
| IDONTWANT threshold | 1,000 B | Classes 1 to 3 trigger it; class 0, at 776 B plus framing, does not. |
| History length and gossip window | 5 and 3 heartbeats (defaults) | Nothing in the design calls for a change. |

StrictNoSign removes the author stamp but does not hide the connection. The ingress Bus Node sees the submitting client's libp2p identity and network address, and later relays see their forwarding peers and the timing. In anonymous mode, the inspected decoder in the vendored 0.50.0 crate rejects `from`, `seqno` and `signature`, but not a message that carries only `key`; the 0.51.0 release adds that check.^[libp2p/rust-libp2p, protocols/gossipsub/CHANGELOG.md, entry for 0.51.0; and protocols/gossipsub/src/protocol.rs, anonymous validation branch; accessed 1 October 2026.] Until the proof of concept adopts that check, it will not be fully StrictNoSign. StrictNoSign also authenticates no Publisher and gives no replay protection; the sealed signature and the accepted set provide those.

The mesh tuple satisfies the v1.1 rules `D_low ≤ D ≤ D_high`, `D_out < D_low` and `D_out ≤ D/2`, and the proof of concept will check them at start-up. The inspected Go library instead requires `D_out < D/2` and rejects 4 at D = 8, so Go interoperability under this profile is not established. Mesh bounds do not cap who sees a message either, because gossip to peers outside the mesh, explicit peers and mesh repair all widen that set. Outbound links resist capture through inbound connections only when honest dial sources exist; poisoned discovery and colluding outbound peers remain risks.

With flood publishing on, a router sends a message it originates to every connected peer whose score is high enough, not only to its mesh. Turning it off gives up part of the publication resilience that v1.1 recommends. It conceals nothing from the ingress Bus Node, which sees the submission either way, and it establishes no source anonymity.

The Rust and Go libraries compare the IDONTWANT threshold differently. Rust tests the serialized GossipSub message length with a strict greater-than; Go tests the payload length, sends at equality, and defaults to 1,024 B. The "IDONTWANT off" setting in Chapter 9's experiments will raise Rust's threshold to 65,537 B, which stops sending notices for frames within the cap but does not stop receiving or honouring them. Sending a message despite a notice must not be penalized. The profile does not yet fix a per-peer, per-heartbeat limit on IDONTWANT messages.

The 65,536 B limit applies to an encoded RPC, including batched messages and control fields, and Go must set it explicitly because its default is 1 MiB. The application's length check on Envelopes (step 6 of Table 8.4) is a separate check on a different object.

The crate's default message identifier is the author plus the sequence number.^[libp2p/rust-libp2p, protocols/gossipsub/src/config.rs, default `message_id_fn`; libp2p-gossipsub 0.50.0 and 0.51.0 source, accessed 1 October 2026.] Both are absent under StrictNoSign. The crate substitutes fixed values for them, so every message would share one identifier and all but the first would be dropped as duplicates. The EID would be the natural replacement, but it fails because of the order of work in rust-libp2p: the router sends IDONTWANT and inserts the identifier into its duplicate cache before the application validator has spoken.^[libp2p/rust-libp2p, protocols/gossipsub/src/behaviour.rs, function `handle_received_message`; libp2p-gossipsub 0.50.0 and 0.51.0 source, accessed 1 October 2026.] The EID excludes the Admission Slot. An attacker could copy an honest Envelope, corrupt its slot and send it first, and the corrupted copy's identifier would be cached; the honest copy, with the same EID, would then be dropped as a duplicate. Hashing the complete Envelope gives the corrupted copy its own identifier, and the honest copy goes through.

The hash input is exactly the Envelope carried as the GossipSub message's data field. It excludes protobuf framing, the GossipSub topic, RPC batching, Noise and Yamux, and every Bus Node must hash the same bytes. This closes that one collision path, assuming a collision-resistant hash; it does not guarantee delivery against other attacks. The EID is still used everywhere else: for the accepted set, for admission binding and for Anchors. The proof of concept will include a switch that uses the EID as the message identifier, only to reproduce the attack in Chapter 9.

### Peer scoring

Each Bus Node keeps a score for every peer it is connected to, computed locally from that peer's behaviour on each GossipSub topic and never shared. Table 8.6 names the components except P5, an application-specific score that the Bus Node sets itself. As a peer's score falls past the three thresholds, the Bus Node first stops exchanging gossip with it, then stops sending it the messages it publishes, and finally ignores everything it sends (the graylist). Scoring follows GossipSub v1.1 [@2020-gossipsub-v11-spec] with one departure. Table 8.6 gives the parameters for each Shard's GossipSub topic, each with topic weight 1.

| Parameter | Value | Effect |
|---|---|---|
| Thresholds: gossip, publish, graylist | −10, −50, −80 | A peer with no other contribution, on one Shard and before decay, falls below them at 2, 3 and 3 invalid messages |
| Opportunistic graft threshold | 5 | Compared with the median total score of mesh peers |
| Topic score cap | 32 | Caps the summed topic contributions after P4 is subtracted |
| P1 time in mesh | 1/360 per second, cap 3,600 s | At most +10 per Shard |
| P2 first deliveries | weight 1, decay 0.99 per second, cap 20 | At most +20 per Shard; rewards useful forwarders |
| P3, P3b mesh delivery deficit and failure | weight 0 | Replaced by application eviction |
| P4 invalid deliveries | weight −10 on the squared count, decay 0.99 per second | 1 invalid: −10; 2: −40; 3: −90 |
| P6 IP colocation | weight −10, threshold 10 | Loopback is whitelisted in local runs |
| P7 behaviour penalty | weight −10, threshold 6, decay 0.9 | Broken IHAVE promises, GRAFT during backoff |
| Score retention | 3,600 s, decay to zero at 0.01 | Disconnecting does not reset a bad score |

The figures in the Effect column are isolated, undecayed arithmetic, not guarantees. Thresholds act on total score with a strict "below" comparison. The P4 counter decays by 0.99 per second, a half-life of about 69 s, so the squared penalty halves in about 34.5 s. Rust applies P7 as `−10 × max(counter − 6, 0)²`, so the first six behavioural faults cost nothing. The opportunistic graft threshold concerns median total score: P1 alone takes 30 minutes to reach 5, while P2 can reach it sooner.

The topic cap is weaker than its name suggests. GossipSub sums the weighted contributions of every GossipSub topic, invalid-delivery penalties included, and only then applies the cap; it does not cap banked positive score before the penalties. With one Shard the largest positive contribution is 30 (P1 10, P2 20), so the cap never binds. With eight Shards the uncapped sum can reach 240, and four undecayed invalid deliveries on one Shard (−160) still leave the capped total at 32. Positive score earned on other Shards can therefore absorb invalid messages. Whether the scoring is safe across every supported Shard configuration is not established, and Chapter 9 lists the test.

P6 can also penalize honest peers that share an address behind NAT, a hosting provider or a proxy. The loopback exemption used in local runs says nothing about the right production policy.

P3 is off, for two reasons. The crate's default topic parameters enable it with a threshold of 20 deliveries and a 5 s activation.^[libp2p/rust-libp2p, protocols/gossipsub/src/peer_score/params.rs, `impl Default for TopicScoreParams`; libp2p-gossipsub 0.50.0 and 0.51.0 source, accessed 1 October 2026.] The complete default profile does not drive idle peers negative: its P1 can reach 3,600 against an idle P3 penalty of −400, and at topic weight 0.5 the sum is +1,600. This profile's P1 is small, however (at most +10), and with it the default P3 penalty of −400 on an idle Shard makes every honest mesh peer's score negative and empties the mesh. The second reason is that formal analysis of GossipSub scoring found parameter sets under which attackers who withhold messages keep positive scores [@2022-kumar-gossipsub-formal; @2023-kumar-gossipsub-acl2s]. The property has to hold for this design's own rule; it cannot be inherited.

The replacement is a simple eviction rule. A heartbeat is "loaded" for a Shard if the Bus Node accepted at least one Envelope on it during that heartbeat. A mesh peer that has not been the first to deliver any accepted Envelope for 90 consecutive loaded heartbeats gets an application score (P5) of −20 for the 60 s prune backoff. The specification asks for delivery "within the mesh delivery window". The proof of concept will approximate it with "first at least once in 90 loaded heartbeats", because ordinary rust-libp2p message events report only first deliveries. The crate also has a delivery-time callback (`with_peer_score_and_message_delivery_time_callback`) that reports peer, GossipSub topic and relative delivery time. It carries no message identifier and can fire before acceptance, so matching it to accepted Envelopes would need extra correlation.

Under uniform latency an honest peer among 8 is first for about one Envelope in 8, which makes 900 Envelopes in a row without a first delivery improbable at 10 per second. With independent deliveries the chance that the peer is never first in 900 Envelopes is (7/8)^900, about 10^-52. At one Envelope per loaded heartbeat the run is 90 Envelopes, and (7/8)^90 is about 6 in a million. Uniform latency is an assumption. Topology and latency can consistently favour other peers, so a slow honest peer may be evicted. Chapter 9's tests of the rule need asymmetric latency, slow honest peers, every Shard and at least 90 loaded heartbeats.

The relay list in the Bus Registry defines who may join a mesh, and a peer not on the list gets −20. The intent is to refuse its GRAFT while keeping it above the graylist, so that the Envelopes it publishes are still validated rather than dropped. As specified for the proof of concept, the −20 is added to the GossipSub score and works through the total, which positive topic contributions can offset: a peer at the per-Shard maximum of +30 still scores +10, keeps its mesh place and can GRAFT. The fixed −20 therefore does not guarantee exclusion or eviction. An application score of −33, which exceeds the largest capped topic contribution of 32, would make the total negative whenever P6 and P7 are not positive; the reference system does not specify it. A per-Shard exclusion would need per-Shard enforcement, because the application score applies to every mesh at once. An `--open` switch will remove the allow-list for adversarial runs.

### What GossipSub does not provide

GossipSub carries opaque bytes, deduplicates them for a bounded time and spreads them through meshes. The reference system claims nothing more from it.

GossipSub provides no anonymity of any kind. The ingress Bus Node sees the submitting endpoint directly, and neighbours see possession times through IHAVE, IWANT and IDONTWANT. Separate sidecar keys avoid reusing the Midnight node's key, but shared hosts, addresses and traffic can still link the two processes. Identify will not be enabled in the proof of concept; a deployment that enables it also leaks the public key, addresses, protocol list and version fields that it sends. Local scoring keeps per-peer and per-Shard observations even when application logs omit them.

GossipSub does not enforce expiry. The stock IWANT handlers serve validated cached messages without reading the MPE Envelope's expiry. The cache holds 5 heartbeats, so the window is seconds, but whether the proof of concept's IWANT path ever sends an expired Envelope is a question it must answer. Expiry also deletes nothing from an adversary's archive: a recorded ciphertext stays recorded, and under a profile without forward secrecy a later key compromise exposes it.

Retention, receipts, Anchors, replay protection, reconciliation and a network-wide quota are Midnight Express mechanisms, described in the next sections. Inventories and Anchors expose some omissions but cannot prove that every Envelope reached a store or remains retrievable.

GossipSub has no discovery it can vouch for. Bus Registry records and authenticated bootstrap records provide identities and addresses. The inspected Rust peer exchange passes peer identifiers but not signed address records, and with the default `prune_peers` of zero it suggests no peers at all. Signed-record peer exchange and zero-degree bootstrappers are outside the proof of concept. A compromised Bus Registry steward, correlated Bus Operators or poisoned address sources can still isolate a Bus Node despite outbound quotas.

Interoperation between the Rust and Go libraries under this profile is not established. Their code differs in the custom protocol identifier, the default version lists, the outbound-quota check, the IDONTWANT predicates and peer-exchange support.

The last gap is the closure of CVE-2022-47547 for the pinned release and this scoring profile. The CVE is a score-manipulation attack found by formal analysis of GossipSub's scoring [@2023-kumar-gossipsub-acl2s], and its closure remains unknown until configuration-specific evidence exists.

## Storage and back-fill

GossipSub keeps a message for only a few heartbeats, so a Subscriber that was offline, or whose feed dropped an Envelope, needs another source. A Store Node keeps what its own validator accepts, keyed by `(expiry, EID)` per Shard, and prunes a record once its expiry is reached. The retention deadline is the visible expiry, so every Store Node agrees on it without coordination. The proof of concept's store will be in memory with a 256 MiB cap; production assumes 32 GiB per Shard. That store will not survive a restart, and receipts make no durability claim. Each Bus Node also keeps a ring of accepted Envelopes for its feed, capped at 64 MiB and 50,000 rows per Shard. The feed is a custom request-response service, not a GossipSub subscription.

Back-fill asks for a Shard from a cursor up to a time. The cursor is `(expiry, EID)`, formed from header fields only, and it means the same thing at every Store Node, so a client can resume at a different Bus Operator. The response is up to 64 Envelopes and a continuation cursor. The request carries no Recognition Tag, stream filter or identifier list, and a Store Node therefore learns which Shard and period a client wants and nothing about which streams. A Store Node that cannot serve the whole range answers `Refused`, `ResourceExhausted` or `RetentionGap` rather than an empty page, so a gap is never silent. A client resuming steps back 60 s from its cursor and drops repeats by EID, which covers Envelopes accepted out of expiry order.

Inventory returns every retained EID in a 60 s window, in pages of 64. Receipts return, for every retained EID in a window, an Ed25519 signature by the Bus Operator over `"mpe/v1/receipt" || N || EID || shard || deadline`. Both are requested by window, for every Envelope, never for the ones a client recognized; asking per Message would tell the Store Node which Envelopes were the client's. A client marks a Message `stored` when receipts from three distinct Bus Operator organizations name the same EID and deadline.

Reconciliation joins storage to delivery. Every 60 s the client fetches the inventory of the recent past from a Store Node whose Bus Operator differs from its feed source. It compares that inventory with every EID it received, matched or not, and back-fills each window with a missing EID. Fetching whole windows rather than single Envelopes keeps the back-fill request free of identifiers. The requirement set asked both for gap repair and for requests that reveal no interest, and only this form satisfies both.

Reconciliation repairs losses that the overlay itself leaves in place. Suppose a Bus Node Ignored an Envelope as `Busy`. An identical copy stays suppressed at that Bus Node while its identifier is in the router's seen cache, because the identifier was cached before validation, and neither Reject nor Ignore removes the entry. That lasts 60 s in this configuration and 120 s under Go's default. Mesh peers do not resend afterwards, so in practice repair from a second source recovers the loss; a later, still-eligible retransmission after the cache entry expires would also succeed. Queue bounds, validation deadlines and IDONTWANT races can cause similar gaps, and a `Busy` reply alone does not repair every affected Subscriber. An unreplicated exploratory observation suggested that an interval of 10 to 15 s repairs such gaps sooner than 60 s (Chapter 10). Chapter 11's churn matrix (experiment 5) tests intervals of 5, 15 and 60 s against a threshold of at least 99.9% of pairs delivered within 10 s.

## Anchors and contract consumption

A Merkle tree hashes a list of items in pairs, then hashes the results in pairs, up to a single root. Anyone holding one item and one sibling hash per level can recompute the root, which shows the item is in the list without revealing the rest. Every Bus Node assigns an Envelope to the window `floor((expiry − 172,800) / 60)`, its creation minute. The window is computed from the header and not from arrival time, so all Bus Nodes agree. Twenty seconds after a window closes, the anchorer computes a Merkle tree per Shard over the window's accepted EIDs in ascending order. It uses the RFC 6962 construction: leaf `SHA-256(0x00 || EID)`, interior node `SHA-256(0x01 || left || right)`, empty tree `SHA-256("")`. The prefix bytes stop anyone presenting an interior node as a leaf. The window root is the same construction over the per-Shard roots in Shard order.

One mock transaction then records the Anchor in Bus Registry state and emits a single `Misc` event. The event carries the window number (8 B), the window root (32 B) and a 4-byte count per Shard: 44 B at one Shard and 72 B at eight. The compiled Bus Registry always carries eight count slots, so its payload is 72 B whatever the Shard count. Both fit the 256-byte `Misc` payload.^[LFDT-Minokawa/compact, compiler/midnight-events.ss, event type `Misc` (name `Bytes 32`, payload `Bytes 256`); main branch, accessed 1 October 2026.] Empty windows produce no Anchor. The Bus Registry keeps 2,940 live Anchors, 49 hours of one per minute, and prunes older ones.

The compiled contracts name this event `mpe/anchor/v1`, and the proof of concept's mock will use the same name. The specification follows the convention of MIP-0018, in which the event name carries the layout version [@midnight-mip-0018]: `mip-xxxx:anchor[v1]`, NUL-padded to 32 bytes, with a new name for each new layout. The Anchor's authority is the Bus Registry state record. The `Misc` copy is a notification, because events are not consensus state [@midnight-mip-0002], and a reader checks Anchors against Bus Registry state.

A Subscriber labels Messages `final` without disclosing which ones it holds. It recomputes the window's root from its own inventory, and if the counts and root match a finalized Anchor, every Message it holds from that window is final. If not, it fetches the anchorer's full leaf list for the window and Shard, checks it against the Anchor, and labels the Messages the list contains. It never asks for a path to one EID. The Ledger Adapter is the client's interface to Midnight state and transaction submission. It acts only on finalized state, so a reorganization never forces a label back. If MPS-0028 produces a best-chain Indexer view [@midnight-mps-0028], an `in-block` label with rollback could be added. The proof of concept will have none.

Only a Consumer that has decided to disclose a Message to a contract asks for an inclusion path. The path runs from the leaf to the Shard root and from the Shard root to the window root. A full minute at 10 Envelopes per second gives 600 leaves, which need 10 levels (2^9 = 512 < 600 ≤ 1,024 = 2^10), and eight Shards add 3 more, so the path is 13 hashes: 10 × 32 B + 3 × 32 B = 416 B.

The reaction constructor produces a transaction to the target contract carrying the signed statement, the Publisher's signature, a consumption nullifier `SHA-256("mpe/v1/consume" || N || contract || Message secret)` and, optionally, the inclusion path. The consumption nullifier lets the contract act on a Message at most once: the contract records it, and a second reaction to the same Message presents the same value. The mock contract will accept only if:

- the statement's destination and action match the contract;
- the signing key is in the contract's Publisher set;
- the expiry is consistent with creation time and still in the future;
- the consumption nullifier is new;
- the inclusion path, when present, verifies under a live finalized Anchor.

The consumption-nullifier insert and the effect happen in one state transition, so racing reactions to one Message produce at most one effect.

The binding here is a Publisher signature plus an Anchor over identifiers, not a contract-execution binding. A Message is not a claim by any contract, and nothing in a reaction can stand in for "this contract emitted this field". A carried event would keep the binding of its own transaction transcript.

The mock contract will have a gap that a Midnight contract must close in circuit. From the transaction alone, it cannot check that the consumption nullifier belongs to the statement, because the consumption nullifier comes from the Message secret and the transaction carries no secret. The mock will look the expected consumption nullifier up in a relation table registered outside the transaction. In Midnight that relation must be proved in zero knowledge inside a Compact circuit.

The exploratory Compact consumer covers only the inclusion half of that circuit. Its circuit, `react(notAfter, action)`, takes the following private witness data:

- the EID and the window;
- a 12-step RFC 6962 path to the Shard root and a 3-step path to the window root;
- a path in the Bus Registry's Anchor tree;
- the Message secret.

The consumer checks the chain from the EID to an Anchor-tree root and asks the Bus Registry, in a second contract call, whether that root is valid. It checks the expiry privately; publicly, it compares the block time only with a coarse bound `notAfter` that the prover chooses. It then derives the consumption nullifier, refuses a known one, and records the consumption nullifier and the action in one transition. It discloses the Anchor-tree root, `notAfter`, the consumption nullifier and the action, and keeps the EID, window, Shard, paths and secret private. It compiles to 77,905 rows (k = 17), plus a k = 6 proof for the Bus Registry's root check.

The circuit shows that an inclusion path confers no authority to react. Nothing in it binds the Message secret to the EID, so anyone holding an inclusion path could react several times with different secrets. The binding needs a Publisher signature verified in circuit over a statement that names the EID or the Logical Message Identifier, which is the production default of `DEC-022`. That circuit has not been written. Compact offers `ed25519Verify`, behind a feature flag for the newer proof format, but MIP-0013 rejects Ed25519 in circuit because emulated field arithmetic needs hundreds of constraints per field operation [@midnight-mip-0013]. A JubJub Schnorr signature profile therefore has to be measured next to it. The size and proving time of the signature circuit remain unknown until it is written and measured.

The compiled contracts also bear on a hashing question. Run in the Compact simulator, `persistentHash` over `Bytes` values, and over structs of `Bytes` fields, gave the same digest as plain SHA-256 of the concatenated bytes, so a contract can recompute the EID chain and the RFC 6962 paths. The simulator runs generated JavaScript, not the circuit constraints, and agreement of the constraints themselves is untested. The encoding that `persistentHash` hashes is documented as unstable [@midnight-mps-0042], so the observation holds only for the toolchain that produced it.

## The ledger lane

The ledger lane is a last resort, and only the application can select it; the client never switches to it silently. For classes 0 to 2, the Publisher creates one transaction to the shared ledger-lane contract. Its transcript emits 4^c `Misc` events (class c has a Sealed Body of 256 × 4^c bytes): 1, 4 or 16 parts, each carrying the next 256 bytes of the Sealed Body. The proof of concept will name the parts `mpe/env/v1`, and the specification names them `mip-xxxx:envelope[v1]`, NUL-padded to 32 bytes. Class 3 would need 64 parts and is refused before any transaction is constructed. No Admission Slot travels on the ledger, so the transaction fee is the only rate limit. Each part is well under the virtual machine's 1 KiB limit, above which events are dropped without error.^[midnightntwrk/midnight-ledger, onchain-vm/src/vm.rs, constant `MAX_LOG_EMITTED`; ledger 9.1 release candidate pinned by the Midnight node, accessed 1 October 2026.]

The parts form a multipart package in the sense of MIP-0019, which is Proposed [@midnight-mip-0019]; on the ledger lane the Publisher is a MIP-0019 publisher and the Subscriber a MIP-0019 reader. A Midnight transaction has a guaranteed segment and fallible segments. If the guaranteed segment fails, the whole transaction fails, whereas a fallible segment can fail alone while the fee is still paid. MIP-0019 requires every part of a package to use one execution phase of one physical intent, because a failing fallible phase discards its events. It recommends the guaranteed phase without requiring it. The mock will place every part in the guaranteed segment.

The cost model of the compiled ledger-lane contract shows that a real ledger would not always allow this. A transcript without a checkpoint goes into the guaranteed segment only if its modelled cost fits the time-to-dismiss budget, which bounds the work a Midnight node spends on a transaction before it knows whether any fee is paid. The 16-part call does not fit (27.6 ms against 25.8 ms, derived: 2 µs × 12,920 B), so its parts land in the fallible segment. That is still one phase, which MIP-0019 accepts, and the requirement therefore reads "in one phase of one intent". A Publisher treats a package as published only after confirming that the transaction was included and that its phase succeeded. The rule of 1, 4 or 16 parts is an application validity rule layered above the multipart transport.

A ledger-lane Subscriber polls the Indexer every second for the lane contract's events, filtered by contract address only. It groups parts by contract, name, transaction and physical intent in emission order, discards groups whose size is not 1, 4 or 16, and runs the same Recognition Tag test and open on the reassembled body. Its Ledger Adapter translates the Indexer's monotonic event `id` into the lane cursor. It reconstructs header bytes 0 to 7 from the event name, the part count, the stream secret and the signed creation time, then delivers with carrier `ledger`. The Indexer sees whole-contract reads and nothing that identifies a stream.

In the proof of concept the reader will label the Message `final` at once, because the mock Indexer will serve only finalized blocks and is trusted. The specification asks for more. The Indexer is a service, and Ledger events are not consensus state, so a lane body is `final` only after its bytes are checked against authenticated on-chain data [@midnight-mip-0018, sec. 7.3], either from the required number of independent chain sources (`P-NET-14`) or by replay. The proof of concept's reader must also be checked against the normative vectors of MIP-0019, and a reader that agrees with them could count toward the readers MIP-0019 requires before acceptance.

The capacity is small. The mock will size a transaction at 8,192 B plus 288 B per `Misc` event, a size borrowed as an assumption from the Anchor sizing and not a Midnight measurement. The 288 B are the struct data of one `Misc` event (a 32-byte name and a 256-byte payload), not its serialized size; MIP-0002 puts the `VersionedLogItem` overhead at about 40 B [@midnight-mip-0002]. The cost model of the compiled contracts gives better inputs:

- a 4,368-byte contract proof;
- a 2,912-byte spend proof for DUST, the non-transferable resource that pays Midnight fees;
- about 700 to 900 B of other transaction bytes;
- about 306 B per `Misc`.

With 800 B for the other bytes, a class-0 transaction comes to about 8,400 B (4,368 + 2,912 + 800 + 306) and class 1 to about 9,300 B. For class 2 the cost model gives about 12,920 B for the 16-part call. Each is close to the mock's 8,480, 9,344 and 12,800 B.

Table 8.7 turns those sizes into capacity under each limit that could bind. `block_usage` counts the bytes a block's transactions occupy, `bytes_written` the net growth of ledger state, and `bytes_churned` bytes written and deleted again. Each figure is the block budget divided by the bytes per Message, rounded down, then divided by the 6 s block time; for example, 1,000,000 / 8,400 gives 119 class-0 transactions per block, 19.8 per second. All figures are derived and assume that no other transaction uses the block. Fees in parentheses include the wallet's margin of 5 blocks of price rise, a factor of about 1.25.

| Class | Parts | Transaction (B) | Per block at `block_usage` 1,000,000 B | Per block at `block_usage` 200,000 B | Per block at `bytes_written` 50,000 B, MIP-0002 sizing | Lane circuit | Fee, DUST (with wallet margin) |
|---|---:|---:|---:|---:|---:|---|---|
| 0 | 1 | about 8,400 | 119 (19.8/s) | 23 (3.8/s) | 152 at 328 B (25.3/s) | k = 18, 166,241 rows | 0.129 (0.161) |
| 1 | 4 | about 9,300 | 107 (17.8/s) | 21 (3.5/s) | 38 at 1,312 B (6.3/s) | k = 20, 663,950 rows | not derived |
| 2 | 16 | about 12,920 | 77 (12.8/s) | 15 (2.5/s) | 9 at 5,248 B (1.5/s) | about k = 22, about 2.65 million rows | 0.188 (0.236) in one call; 0.866 (1.084) as 16 calls |
| 3 | 64 | refused | | | | | |

Which limit binds is not settled. The Midnight node's network configurations set `block_usage` to 1,000,000 B, while the ledger's initial limits set it to 200,000.^[midnightntwrk/midnight-node, res/mainnet/ledger-parameters-config.json, `block_limits`; and midnightntwrk/midnight-ledger, ledger/src/structure.rs, `INITIAL_LIMITS`; main branch, accessed 1 October 2026.] Which value is live is unknown. MIP-0002 sizes event throughput against the shared `bytes_written` budget of 50,000 B per block, which gives the column in the table [@midnight-mip-0002]. In that column each part costs 328 B, the 288 B of struct data plus MIP-0002's 40 B of overhead, so a class-1 Message costs 4 × 328 = 1,312 B.

The ledger-9 code charges logged bytes differently. Its `Log` instruction counts every logged byte as both written and deleted, and the block limit applies to net written bytes, the larger of zero and written minus deleted. Logged bytes therefore fall on the `bytes_churned` budget, which is 50,000,000 B per block in the Midnight node's network configurations and 1,000,000 B in the ledger's initial limits.^[midnightntwrk/midnight-ledger, onchain-vm/src/vm.rs, `Log` arm of the interpreter; and base-crypto/src/cost_model.rs, conversion of running cost to synthetic cost; ledger 9.1 release candidate and main branch, accessed 1 October 2026.] The Compact simulator's cost accounting agrees: the 16-part call writes 224 B net and churns 26,931 B. MIP-0002 itself states both that log bytes count as churn and that events compete for `bytes_written`. Under the code's reading, `block_usage` binds.

This document plans with the lower figures. For the whole chain that is about 6.3 class-1 and 1.5 class-2 Messages per second; for class 0 it is the `block_usage` figure, 19.8 or 3.8 per second depending on the live value. Two measurements would settle both questions: the serialized size, `bytes_written`, churn and fee of 1-, 4- and 16-part groups, taken on a ledger-9 devnet or on Stagenet, Midnight's staging network. The mock will enforce only a 1,000,000 B `block_usage`. Against the MIP-0002 sizing it overstates class-1 and class-2 capacity by about 3 and 9 times (derived: 17.8 / 6.3 and 13.0 / 1.5).

Proving adds latency and cost that the mock does not have. Each part is public data that a circuit must turn into bytes, and emitting a 256-byte circuit argument costs 166,241 rows (k = 18), against 23 rows for a constant payload. The k = 18 proving keys are 67 to 76 MB, and generating the key for one part took 264 s and 1.8 GB of memory when the contract was compiled. Sixteen parts in one call cost less in fees than sixteen calls (0.188 against 0.866 DUST) but need a k = 22 circuit, so the requirement set considers lowering the in-contract limit to 4 parts (k = 20) unless a cheaper `Misc` encoding appears. Latency is proving time, which is unknown, plus the wait for inclusion, plus 18 s to finality, plus up to 1 s of polling. With inclusion in the next block, everything but proving comes to at most 6 + 18 + 1 = 25 s.

The ledger lane also depends on a ledger generation that mainnet did not run on 4 August 2026, when it ran ledger 8.0. Contract events arrive with ledger 9, and MIP-0002 is live on Stagenet. The compiler that supports `emit` states that it targets ledger 9, not yet deployed on mainnet.

## The ledger interface in Compact

Compact is Midnight's language for contracts. The Bus Registry, the ledger-lane contract and a contract consumer were written in Compact as exploratory code and compiled with toolchain 0.35.0 (language 0.27.0, a ledger-9 release candidate, compact-runtime 0.20.0). The design does not depend on these contracts being final. Nothing ran on a Midnight network: no transaction was constructed, proved, balanced or submitted, and no proof was generated or verified. Circuit sizes come from the compiler's circuit model. Fees are derived from the ledger-9 cost model at genesis prices with estimated block bytes. The generated JavaScript was also exercised in the Compact simulator on:

- registration and relay management;
- Anchor posting with five refusal cases, and the historic Anchor-root check;
- revocation and its refusals;
- pause;
- the 16-part lane call and the refusal of a foreign `Misc` name.

That exercise runs the generated JavaScript, not the circuits, and it does not run the consumer's cross-contract call.

The Bus Registry, the lane contract and the consumer each compile with 0.35.0. With the ledger-8 toolchain (0.31.1), the Bus Registry and the lane contract fail on `emit`, which needs toolchain 0.33 or later. Without its two `emit` statements the Bus Registry compiles there too, so `emit` is its only ledger-9 dependency. The consumer fails with 0.31.1 because of the older cross-contract model. Every proof in the model is at most 4,368 bytes and every verifying key at most 2,119 bytes, while proving keys grow with k. Table 8.8 gives the main circuits.

| Contract and circuit | k | Rows | Fee, DUST (with wallet margin) | Note |
|---|---:|---:|---|---|
| Bus Registry `register` | 13 | 6,305 | 0.246 (0.308) | About 8,670 B; inside the requirement set's registration gate (`P-ECO-13`) of 16 KiB and 0.5 DUST |
| Bus Registry `postAnchor` | 18 | 152,138 | 0.195 (0.244) | About 280 DUST per day at one Anchor per 60 s (derived: 1,440 × 0.195) |
| Bus Registry `revoke` | 17 | 77,971 | not derived | Checks the RLN relation on two shares and the member's path |
| Bus Registry `addRelay`, `removeRelay`, `setSteward` | 17 | about 67,000 | not derived | Cost is in the governance `Misc` payload bytes |
| Bus Registry `pause`, `unpause`, `proposeParams` | 15 | about 27,000 | not derived | |
| Bus Registry `anchorRootValid` | 6 | 46 | not derived | Witness-free, callable by another contract |
| Ledger lane `publishClass0` | 18 | 166,241 | 0.129 (0.161) | One part |
| Ledger lane `publishClass1` | 20 | 663,950 | not derived | Four parts |
| Ledger lane `publishClass2` | about 22 | about 2.65 million | 0.188 (0.236) | Sixteen parts; key not generated |
| Consumer `react` | 17 | 77,905 | not derived | Plus the k = 6 Bus Registry call |

The compiled Bus Registry keeps the following state:

- one membership tree per membership period;
- a set of revoked commitments;
- the parameters, with a time-locked change path;
- the relay list and the pause flag;
- a hash of the steward secret;
- the Anchors, in a ring of 2,940 slots indexed by `window mod 2940`;
- an Anchor tree that a consumer can check without reading the records.

The registration circuit computes the member's leaf from the current per-class limits, so a registrant cannot choose its own. The relay list is keyed by SHA-256 of the libp2p peer identifier, because an Ed25519 peer identifier is a 38-byte multihash, not a raw 32-byte key. Relay-list changes emit a governance `Misc` named `mpe/gov/v1`; whether these should use that name or the standard `Paused` and `Unpaused` events is open.

Compiling the interface turned up six constraints, each of which changes what the proof of concept's mock must do or what the specification may ask for.

Byte work dominates proving. Every operation that needs individual bytes (a spread, an index, an integer-to-bytes cast, a non-constant `emit` payload) costs about 670 rows. Three chained SHA-256 node hashes give identical digests either way, yet they cost 133,922 rows when the preimage is assembled by spreading bytes and 12,674 rows when it is a struct of `Bytes` fields. Protocol hashes computed in circuit must therefore use struct preimages of fixed-width fields, and circuits should emit as few non-constant bytes as the protocol allows.

There is no signer. A Midnight transaction has no sender, so the steward and the anchorer prove knowledge of a secret whose SHA-256 is in Bus Registry state, and the "submitter key" of a relay entry is that key commitment.

Block time can be compared, not read. Every time-stamped write takes a clock value from the caller and checks it against the block time within a tolerance (900 s in the compiled contracts), and a transaction that waits in the pool longer than that fails. The Bus Registry cannot record when a root was published or superseded; readers take those times from the timestamps of the including blocks. Every comparison also discloses its operand, which is why the consumer discloses only a coarse `notAfter`.

The root window cannot be enforced on chain. A circuit cannot read its own Merkle root, and the historic-root check accepts every past root. The 3,600 s root window is enforced by Bus Nodes, off chain.

DUST cannot be paid to a contract. It only pays transaction fees, so a membership costs exactly the network fee of the registration transaction, and a price beyond that would need NIGHT or another token, received shielded or unshielded.

Large transcripts leave the guaranteed segment. By the cost model's gas, registration, Anchor posting and the 16-part lane call all exceed the time-to-dismiss budget, and their events land in the fallible segment, still in one phase.

Two capabilities would make this interface cheaper, and neither exists: a cheaper path for emitting public byte payloads, which is the dominant prover cost, and a way to read the block time or a contract's own Merkle root inside a circuit. Proving time and prover memory for the k = 18, 20 and 22 circuits are not measured. The toolchain and the ledger are release candidates of a generation that mainnet does not run, so every number here can change before ledger 9 is deployed.

## What is real and what is mocked

The proof of concept will run some parts for real and stand in for others, as Table 8.9 records part by part.

| Part | Real in the proof of concept | Mocked or absent |
|---|---|---|
| Overlay | libp2p swarms over localhost TCP with Noise and Yamux; GossipSub v1.2 with IDONTWANT, scoring, eviction and the allow-list, under a custom protocol identifier | Wide-area latency, loss, bandwidth limits, NAT, IP diversity; scale beyond tens of Bus Nodes; the standard `/meshsub/1.2.0` profile; the `key` check of StrictNoSign; subscription-name filtering; peer exchange and zero-degree bootstrappers; interoperation with Go |
| MPE Envelope | Wire format, four sizes, sealing, signatures, Recognition Tags, recognition, padding checks and test vectors | A suite identifier; carried events; any forward secrecy or post-quantum profile; a profile aligned with `encrypt_for` |
| Admission | Slot layout, admission-window and root-window checks, admission nullifiers, share binding, per-class limits, equivocation evidence, secret recovery, queue bounds, restart barrier | The zero-knowledge proof: every Bus Node holds every member's secret, can link every publication and can forge admission; verification cost is a 4.5 ms busy-wait |
| Storage | Back-fill, portable cursors, inventory, signed receipts, reconciliation with a second Bus Operator | Durability across restarts; production capacity |
| Ledger | Midnight's block time, finality depth, block and transaction byte limits, `Misc` shape, 1 KiB event rule, no signer and pool longevity, enforced in a mock | The Midnight node, ledger, Indexer, fees, DUST and proving; `bytes_written` and churn limits; fallible-segment placement; transaction sizes are assumed |
| Bus Registry | Roots, relay list, parameters, Anchors and pause flag in mock state; separately, an exploratory Compact contract compiled and costed | Registration transactions on a network; a finalized roster subscription; governance beyond one maintainer key in the mock; bonds |
| Contract consumption | Signed statement, consumption nullifier, inclusion path, single effect under racing reactions; separately, a compiled inclusion-only consumer circuit | The zero-knowledge relation between consumption nullifier and statement, replaced in the mock by a trusted table outside the transaction; the in-circuit signature check, which is not written |

The harness will scan the relay's view of the wire for every secret it knows. A count of zero would say nothing about timing, traffic analysis, connection identities or source anonymity. Because admission is a stand-in, the proof of concept can support no privacy claim about Publishers. It can test the four claims that Chapter 4 makes for a Confidential Message: content confidentiality, sealed labels, no silent change of leakage, and interest privacy conditional on whole-Shard reception and uniform client behaviour. The remaining claims cannot be tested without a real proof system, a ledger-9 network and a real wide-area network.
