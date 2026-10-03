## Scope of this area

CRY owns Event sealing, cryptographic recognition, key derivation, rotation, publisher authentication, nonce safety and cryptographic replay protection.
The recommended Prototype default uses authenticated invitations, symmetric stream secrets, locally tested salted Tags and sealed publisher signatures.
That default makes no forward-secrecy claim; an optional production session profile targets hybrid establishment with encrypted-header Double Ratchet.
Fuzzy detection is not part of the design (`DEC-020`); `MPE-CRY-038` and `MPE-CRY-039` apply only if a separately specified future profile adds it.
Shard selection, transport admission, storage availability and contract execution belong to other areas; cryptography supplies their required bindings.

## Parameters

All defaults are design assumptions unless identified as primitive-defined sizes. Parameters affecting wire encoding are fixed within a cryptographic profile; changing them requires a new profile identifier.

| Parameter | Meaning | Default | Allowed range | Source |
|---|---|---:|---|---|
| P-CRY-1 | Symmetric stream-secret length | 32 bytes | 32 bytes for the default profile | g4 R1 D3; s2 R1 D3; **assumption** selecting their secret width |
| P-CRY-2 | Salted Tag length | 16 bytes | 16 or 32 bytes, fixed per profile | o1 R1 D1/D3; o3 R1 D3; **assumption** for the salted construction |
| P-CRY-3 | Envelope salt length | 16 bytes | 16–32 bytes, fixed per profile | s2 R1 D1; s4 R1 D1; **assumption** adapting the random salt to recognition |
| P-CRY-4 | Maximum distinct active recognition keys per Subscriber device | 256 keys | 1–256 keys | s2 R1 D3; **assumption**, including current, pending and retained keys |
| P-CRY-5 | Maximum skipped-message derivations for one ratcheted session transition | 1,000 keys | 0–1,000 keys | s2 R1 D3; `2016-signal-double-ratchet-spec`, §8.4 |
| P-CRY-6 | Maximum retained skipped-message keys per Subscriber device | 4,096 keys | 0–4,096 keys | s2 R1 D3; **assumption** |
| P-CRY-7 | Maximum skipped-message-key retention after derivation | 604,800 seconds | 0–604,800 seconds | s2 R1 D3; **assumption**; erasure trade-off in `2016-signal-double-ratchet-spec`, §8.4 |
| P-CRY-8 | Experimental FMD2 false-positive probability for unrelated valid clues | 1/32 | \(2^{-n}\), integer \(1 \le n \le 15\) | `2021-beck-fmd`, §7, Table 1; **assumption** selecting the experimental default |

The default profile uses ChaCha20-Poly1305’s 12-byte nonce and 16-byte authenticator, as proposed by g1 and g4 R1 D1. These are algorithm-defined widths, not tuning parameters. The Tag is separate from the AEAD authenticator.

## Requirements

### MPE-CRY-001 Default cryptographic profile

The MPE client library shall implement an invitation-based symmetric profile using HKDF-SHA-256 key derivation, HMAC-SHA-256 recognition, ChaCha20-Poly1305 sealing and plain Ed25519 publisher authentication.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1, D3; g1 R1 D1/D3; g4 R1 D1/D3; s2 R1 D1; o3 R1 D1; **assumption** selecting this combination.
- Rationale: This provides a bounded Prototype default without attributing session guarantees to symmetric stream encryption.
- Verify: test, independent implementations agree on derivation, sealing, recognition and signature vectors.
- Status: open (DEC-CRY-1)

### MPE-CRY-002 Sealed application metadata

The MPE client library shall encrypt the Event’s private stream identifier, publisher identity, schema, logical identifier, sequence, application timestamps, payload and publisher signature inside the Envelope.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; s2 R1 D1; o1 R1 D1; o3 R1 D1; s4 R1 D1.
- Rationale: Relay validation does not require application metadata.
- Verify: inspection, the wire-field inventory contains these fields only within authenticated ciphertext.
- Status: settled

### MPE-CRY-003 Authenticated padding

The MPE client library shall include the padding prescribed by the Envelope’s size class within authenticated encryption.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; g1 R1 D1; s1 R1 D1; s2 R1 D1; o1 R1 D1.
- Rationale: Padding outside authentication would permit undetected alteration of the sealed representation.
- Verify: test, changing any protected padding byte causes authentication failure.
- Status: settled

### MPE-CRY-004 Public-context authentication

The MPE client library shall authenticate the canonical pre-seal header as AEAD associated data, including network identity, Envelope version, cryptographic profile, size class, Shard, expiry, salt, nonce and Tag.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; g1 R1 D1; s2 R1 D1; s1 R2 D1; s4 R2 D1.
- Rationale: Public routing and lifetime fields must not be alterable independently of the seal.
- Verify: test, changing each bound field prevents opening under the original context.
- Status: settled

### MPE-CRY-005 Acyclic Envelope construction

The MPE client library shall construct an Envelope through the dependency order pre-seal header, signed plaintext, ciphertext, admission content commitment, Admission Proof, then final wire identifier.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; s1 R2 D1; s4 R2 D1; objections to g1 and o1 R1 D1.
- Rationale: Admission-dependent fields cannot participate in inputs that must exist before their construction.
- Verify: inspection, the construction dependency graph is acyclic and every cryptographic input exists before use.
- Status: settled

### MPE-CRY-006 Domain separation

The MPE client library shall use distinct canonical domain encodings for Tags, encryption derivation, header derivation, publisher signatures, Envelope commitments, logical identifiers and consumption nullifiers, incorporating network identity and cryptographic profile.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1, D3; g1 R1 D1; s2 R1 D1/D3; o1 R1 D3; `2016-signal-double-ratchet-spec`, §7.2.
- Rationale: A value valid for one purpose must not become valid for another purpose through ambiguous encoding.
- Verify: test, cross-purpose, cross-network and cross-profile substitution vectors fail.
- Status: settled

### MPE-CRY-007 Purpose-specific derivation

The MPE client library shall derive separate recognition and encryption keys from a stream secret using distinct HKDF-SHA-256 purpose labels, with the Envelope salt included in per-Envelope encryption derivation.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1, D3; g1 R1 D1; s2 R1 D1; s4 R1 D1; **assumption** for the salted symmetric profile.
- Rationale: Possession or use of one derived key must not substitute for another cryptographic purpose.
- Verify: test, derivation vectors distinguish purposes, salts, networks and profiles.
- Status: open (DEC-CRY-2)

### MPE-CRY-008 Random stream secrets

When a private stream is created, the MPE client library shall generate its P-CRY-1-byte stream secret from a cryptographically secure random generator.

- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; g4 R1 D3; s2 R1 D3; o3 R1 D3; `2021-len-partitioningoracle`, §1.
- Rationale: Human-selected passphrases expose a different guessing threat from random capabilities.
- Verify: inspection, stream creation obtains the specified bytes from the configured operating-system randomness source.
- Status: settled

### MPE-CRY-009 Randomness failure

If required cryptographic randomness cannot be obtained, then the MPE client library shall refuse the affected cryptographic operation with a local failure result.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D1, D3; s2 R1 D9/D10; `2023-signal-pqxdh-spec`, §4.11.
- Rationale: Predictable replacement randomness invalidates key and nonce assumptions.
- Verify: test, injected entropy failure produces no key, ciphertext or bootstrap publication.
- Status: settled

### MPE-CRY-010 Nonce uniqueness

The MPE client library shall use each AEAD key–nonce pair for at most one encryption operation.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1; g1 R1 D1; g4 R1 D1; s2 R1 D1; `2016-signal-double-ratchet-spec`, §4.2.
- Rationale: Repeated encryption with one pair can invalidate confidentiality or authenticity assumptions.
- Verify: test, forced nonce repetition, concurrent publication and crash recovery cannot produce a second encryption under the same pair.
- Status: settled

### MPE-CRY-011 Unsafe restored state

If restored client state cannot establish nonce uniqueness or ratchet-state freshness, then the MPE client library shall refuse publication under the affected key generation until authenticated re-establishment.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; s2 R1 D9/D10; s3 R1 D3; **assumption** defining the recovery response.
- Rationale: Backup restoration can reintroduce consumed counters, keys or prekeys.
- Verify: test, restoring a pre-publication snapshot prevents subsequent publication under its obsolete generation.
- Status: settled

### MPE-CRY-012 Exact retransmission

When an existing Envelope is retransmitted, the MPE client library shall reuse its original serialized bytes.

- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; s2 R1 D3; s3 R1 D3.
- Rationale: Retransmission does not require another encryption operation or bootstrap transition.
- Verify: test, repeated transmission preserves ciphertext, nonce, Tag and wire identifier.
- Status: settled

### MPE-CRY-013 Salted private Tags

When sealing a private Event, the MPE client library shall generate a P-CRY-2-byte Tag by truncating HMAC-SHA-256 over the canonical Tag domain and a fresh P-CRY-3-byte Envelope salt under the stream’s recognition key.

- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D1, D3; s4 R1 D1; o1 R1 D3; o3 R2 D1; **assumption** selecting salted recognition instead of sequence lookahead.
- Rationale: Recognition does not depend on predicting an unbroken sequence window.
- Verify: test, independent vectors agree; arbitrary publisher-sequence gaps do not prevent recognition under a retained stream key.
- Status: open (DEC-CRY-2)

### MPE-CRY-014 Recognition is provisional

When a Tag or fuzzy clue matches, the MPE client library shall treat the Envelope only as a candidate for complete Event authentication.

- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; s2 R1 D3; o1 R1 D3; `2021-beck-fmd`, §2.
- Rationale: Recognition hints do not establish decryption success, publisher authority or application validity.
- Verify: test, matching hints paired with invalid ciphertext or signatures produce no Event delivery.
- Status: settled

### MPE-CRY-015 Local Tag recognition

The MPE client library shall perform private Tag recognition within the Subscriber’s local trust boundary.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D3; s1 R1 D3; s2 R1 D3; s4 R1 D3; o1 R2 D3.
- Rationale: Giving infrastructure a precise recognition key changes the interest-hiding boundary.
- Verify: inspection, Bus Node and Store Node interfaces receive neither private Tag keys nor Tag-match results.
- Status: settled

### MPE-CRY-016 Recognition-key bound

When installing subscription state would exceed P-CRY-4 distinct recognition keys, the MPE client library shall reject that installation with a local capacity result.

- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; s2 R1 D3; **assumption** applying its bound across supported recognition profiles.
- Rationale: Pending invitations and historical keys consume recognition capacity alongside current keys.
- Verify: test, installation at the limit succeeds; installation beyond the limit leaves existing subscriptions unchanged.
- Status: open (DEC-CRY-2)

### MPE-CRY-017 Ambiguous opening

If one Envelope authenticates as belonging to distinct private streams, then the MPE client library shall reject its delivery with a local ambiguity result.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D1, D3; s1 R1 D1; s4 R1 D1; `2021-len-partitioningoracle`, §1; `2022-grubbs-anonrobustpq`, §1; **assumption** defining the response.
- Rationale: Trial processing must not silently choose between conflicting authenticated interpretations.
- Verify: test, injected multiple-opening vectors produce no delivery to either stream.
- Status: settled

### MPE-CRY-018 Authenticated invitations

When installing a private subscription, the MPE client library shall validate an invitation binding the network, cryptographic profile, stream secret or setup material, and authorized publisher keys through the configured authenticated invitation channel.

- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; s1 R1 D3; s2 R1 D3; s4 R1 D3; `2023-signal-pqxdh-spec`, §4.1.
- Rationale: Confidential bytes alone do not establish which publisher or network the Subscriber intended to trust.
- Verify: test, modified, unauthenticated, foreign-network and unsupported-profile invitations cannot install subscriptions.
- Status: open (DEC-CRY-3)

### MPE-CRY-019 Revocation rekeying

When an authorized membership change removes a Subscriber from a symmetric private stream, the MPE client library shall generate the replacement stream secret independently of the previous stream secret.

- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; g1 R1 D3; o3 R1 D3; s2 R2 D2; **assumption** requiring fresh entropy for revocation.
- Rationale: A removed holder can calculate future secrets obtained solely by hashing its old secret.
- Verify: test, possession of the old secret does not derive the replacement secret or open Events sealed under it.
- Status: settled

### MPE-CRY-020 Publisher signature profile

The MPE client library shall authenticate publisher statements with plain Ed25519 in the default cryptographic profile.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1, D3; s2 R1 D1/D3; g1 R1 D1; `minokawa-compact/doc/api/CompactStandardLibrary/exports.md:993`.
- Rationale: The checked Compact API supports plain Ed25519 and explicitly excludes Ed25519ctx and Ed25519ph.
- Verify: test, library signatures verify over identical statement bytes in a compiled Compact fixture.
- Status: open (DEC-CRY-6)

### MPE-CRY-021 Signed statement binding

The MPE client library shall sign a canonical statement binding the signature domain, pre-seal-header digest, private stream identifier, logical identifier, publisher sequence, schema, creation time, expiry, payload digest and applicable destination contract and action.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1, D3; s2 R1 D1/D3; s3 R1 D3; o3 R2 D3.
- Rationale: A valid publisher signature must not authorize a different payload, network, lifetime or contract action.
- Verify: test, substituting each signed field causes publisher-signature verification failure.
- Status: settled

### MPE-CRY-022 Authenticated delivery

When an Envelope is opened, the MPE client library shall deliver its Event only after validation of the seal, canonical inner encoding, signed context, authorized publisher key and application expiry.

- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D1, D3; s2 R1 D1/D3; s3 R1 D3; o3 R1 D3.
- Rationale: Shared possession of a reading secret does not confer another publisher’s signing authority.
- Verify: test, malformed, expired, unauthorized and signature-invalid Events produce no delivery.
- Status: settled

### MPE-CRY-023 Failure-atomic cryptographic state

When processing an incoming Envelope, the MPE client library shall commit cryptographic state changes only after complete Event authentication succeeds.

- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; s2 R1 D3/D10; `2016-signal-double-ratchet-spec`, §4.6.
- Rationale: Failed body authentication must not consume retained keys or advance a receiving chain.
- Verify: test, invalid bodies following valid-looking headers leave persistent cryptographic state unchanged.
- Status: settled

### MPE-CRY-024 Authenticated logical replay

If an authenticated Event’s publisher, private stream and logical identifier tuple is already present in durable replay state, then the MPE client library shall suppress its repeat delivery.

- Pattern: unwanted
- Scope: POC
- Priority: MUST
- Source: D3; s1 R1 D3; s2 R1 D3; s3 R1 D3.
- Rationale: A new salt, ciphertext or Admission Proof does not make the same logical Event new.
- Verify: test, independently encrypted retries of one authenticated logical Event produce one delivery across restart.
- Status: settled

### MPE-CRY-025 Secret-bearing consumption nullifiers

Where contract-consumption nullifier derivation is supported, the MPE client library shall derive the nullifier from an Event-specific secret using a canonical domain containing the network and destination contract.

- Pattern: optional
- Scope: POC
- Priority: MUST
- Source: D3; o3 R1 D3; s1 R2 D3; s4 R2 D3; **assumption** selecting the corrected secret-bearing construction.
- Rationale: Hashing a public Envelope identifier with a domain remains publicly enumerable.
- Verify: test, the same Event secret reproduces the destination’s nullifier; changing destination changes it.
- Status: settled

### MPE-CRY-026 Explicit security posture

The MPE client library shall expose each profile’s capability record specifying content forward secrecy, key-retention exposure, post-compromise recovery conditions, passive quantum protection, authentication algorithm and metadata-forward-secrecy limitations.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1, D3; g1 R1 D3; s2 R1 D2/D3; s2 R2 D2; `2022-barnes-rfc9180`, §9.1.
- Rationale: The symmetric default reports no forward secrecy; hybrid setup does not make MPE wholly post-quantum.
- Verify: inspection, capability records distinguish the default from ratcheted profiles and state all retained-key exposure.
- Status: settled

### MPE-CRY-027 Seed-restoration boundary

Where wallet-seed derivation is supported, the MPE client library shall restrict seed-restorable derivations to domain-separated bus identity or invitation keys.

- Pattern: optional
- Scope: PROD
- Priority: MUST
- Source: D3; o1 R1 D3; s2 R1 D2/D9; `2016-signal-double-ratchet-spec`, §8.1; **assumption** limiting seed restoration.
- Rationale: Restoring identity must not regenerate supposedly erased message, ratchet or historical stream secrets.
- Verify: inspection, derivation paths cannot reconstruct erasable session state from the wallet seed.
- Status: open (DEC-CRY-1)

### MPE-CRY-028 Encrypted-header session profile

Where ratcheted pairwise sessions are supported, the MPE client library shall seal the complete encrypted-header Double Ratchet packet within the Envelope’s protected representation.

- Pattern: optional
- Scope: PROD
- Priority: SHOULD
- Source: D1, D3; s2 R1 D1/D3; s3 R1 D1; `2016-signal-double-ratchet-spec`, §4.1.
- Rationale: Ratchet public keys, counters and session association must not become clear application selectors.
- Verify: inspection, packet captures contain no clear ratchet header or stable session identifier.
- Status: open (DEC-CRY-1)

### MPE-CRY-029 Ratchet-key erasure

When a ratcheted session transition becomes durable, the MPE client library shall erase superseded secret state outside the declared skipped-key retention policy.

- Pattern: event
- Scope: PROD
- Priority: MUST
- Source: D3; s2 R1 D2/D3; `2016-signal-double-ratchet-spec`, §§8.1–8.4.
- Rationale: Conditional forward secrecy depends on erasure rather than the ratchet algorithm’s name.
- Verify: inspection, post-transition memory and persistent-state inventories exclude used message keys and obsolete ratchet secrets.
- Status: open (DEC-CRY-1)

### MPE-CRY-030 Bounded skipped-key retention

While a ratcheted session is active, the MPE client library shall retain skipped-message keys only within P-CRY-5 derivations per transition, P-CRY-6 stored keys per device and P-CRY-7 seconds after derivation.

- Pattern: state
- Scope: PROD
- Priority: MUST
- Source: D3; s2 R1 D3; s3 R1 D3; `2016-signal-double-ratchet-spec`, §8.4.
- Rationale: Retained keys impose memory costs and expose their corresponding archived ciphertexts after compromise.
- Verify: test, boundary gaps and clock advancement enforce every limit without retaining excess keys.
- Status: open (DEC-CRY-1)

### MPE-CRY-031 Explicit cryptographic gaps

If opening an Event requires erased keys or would exceed a cryptographic key budget, then the MPE client library shall return a local resynchronization-required result.

- Pattern: unwanted
- Scope: PROD
- Priority: MUST
- Source: D3; s2 R1 D3; o3 R1 D3; s2 R2 D3.
- Rationale: Stored ciphertext is not necessarily decryptable after key erasure or unbounded sequence gaps.
- Verify: test, over-limit and erased-key back-fill produces an explicit result without reconstructing obsolete state.
- Status: open (DEC-CRY-1)

### MPE-CRY-032 Hybrid session establishment

Where the hybrid pairwise profile is supported, the MPE client library shall establish sessions using PQXDH instantiated with X25519 and ML-KEM-768, with network, profile, identities and actual KEM public key bound to the bootstrap transcript.

- Pattern: optional
- Scope: PROD
- Priority: SHOULD
- Source: D1, D3; s2 R1 D1/D3; `2023-signal-pqxdh-spec`, §§2.1, 3, 4.10, 4.12; `2024-nist-fips203`, Table 3; **integration assumption**.
- Rationale: Hybrid setup targets passive recorded-ciphertext attacks without claiming quantum-secure authentication or recovery.
- Verify: test, independent bootstrap vectors agree; identity, KEM-key, network and profile substitutions fail.
- Status: open (DEC-CRY-4)

### MPE-CRY-033 Wrapped bootstrap metadata

Where invitation-based hybrid establishment is supported, the MPE client library shall protect bootstrap identity keys, prekey identifiers and initialization material with invitation-derived wrapping keys.

- Pattern: optional
- Scope: PROD
- Priority: MUST
- Source: D1, D3; s2 R1 D3; s2 R2 D1; **assumption** for invitation wrapping.
- Rationale: Setup fields must not become relay-visible recipient or session selectors.
- Verify: inspection, bootstrap captures reveal no identity key or prekey identifier outside the protected representation.
- Status: open (DEC-CRY-4)

### MPE-CRY-034 One-time prekey consumption

When a bootstrap authenticates successfully, the MPE client library shall erase its used one-time prekey private material after durably recording that bootstrap’s identity.

- Pattern: event
- Scope: PROD
- Priority: MUST
- Source: D3; s2 R1 D3; `2023-signal-pqxdh-spec`, §§3.4, 4.2–4.3.
- Rationale: Replay must not recreate a session from already consumed one-time material.
- Verify: test, concurrent duplicate bootstraps and restart yield at most one initialization and no remaining consumed private prekey.
- Status: settled

### MPE-CRY-035 Establishment failure

If required one-time prekeys are exhausted, bootstrap authentication fails or selected-profile input validation fails, then the MPE client library shall refuse establishment without selecting a weaker profile.

- Pattern: unwanted
- Scope: PROD
- Priority: MUST
- Source: D1, D3; s2 R1 D1/D3; `2023-signal-pqxdh-spec`, §§3.3–3.4, 4.9; **assumption** excluding last-resort fallback.
- Rationale: Unavailable setup material does not authorize a confidentiality or forward-secrecy downgrade.
- Verify: test, exhausted, corrupted and downgrade vectors create no session under any alternative profile.
- Status: open (DEC-CRY-4)

### MPE-CRY-036 Cryptographic size and cost report

The Prototype shall report serialized cryptographic component sizes, complete Envelope sizes, usable payload capacity, operation-time distributions and peak cryptographic-state bytes for every implemented profile at its configured key limits.

- Pattern: ubiquitous
- Scope: POC
- Priority: MUST
- Source: D1, D3; s2 R1 D1/D10; o1 R2 D1; s2 R2 D1/D3; `2024-nist-fips203`, Table 3; `2024-nist-fips204`, Table 2.
- Rationale: Primitive sizes do not establish complete Envelope capacity or MPE performance.
- Verify: demonstration, a reproducible report accounts for every serialized byte and gives operation times in microseconds and state sizes in bytes.
- Status: settled

### MPE-CRY-037 Fuzzy-detection activation

When initializing a client configuration without explicit first-contact FMD opt-in, the MPE client library shall leave fuzzy detection disabled.

- Pattern: event
- Scope: POC
- Priority: MUST
- Source: D3; s2 R1 D3; o3 R1 D3; o4 R2 D3; `2021-seres-fmdfalsepositives`, §§1, 4–6.
- Rationale: Delegated fuzzy detection introduces a distinct leakage model and does not replace authenticated invitations by default.
- Verify: test, default configurations generate no fuzzy clue or delegated detection registration.
- Status: open (DEC-CRY-5)

### MPE-CRY-038 Restricted detection delegation

Where first-contact FMD delegation is enabled, the MPE client library shall export only the selected construction’s first-contact detection capability to the detector.

- Pattern: optional
- Scope: PROD
- Priority: MUST
- Source: D3; o1 R1 D3; s2 R1 D3; `2021-beck-fmd`, §2; `2022-penumbra-fmd-spec`, “Sender and Receiver FMD”.
- Rationale: Delegation excludes Event-decryption keys, precise stream-Tag keys, signing keys and established-session state.
- Verify: inspection, detector registration contains only construction-defined first-contact detection material.
- Status: open (DEC-CRY-5)

### MPE-CRY-039 FMD construction measurement

Where experimental FMD2 is implemented, the Prototype shall report clue size, generation time, testing time, true-match failures and observed unrelated-clue match frequency at P-CRY-8.

- Pattern: optional
- Scope: POC
- Priority: MUST
- Source: D1, D3; s2 R1 D3; o2 R2 D3; `2021-beck-fmd`, §7, Table 1.
- Rationale: Beck’s benchmark is evidence about FMD2, not an MPE result or a Penumbra clue-size specification.
- Verify: demonstration, a labeled-corpus report states sample counts, configuration, hardware and frequency uncertainty.
- Status: open (DEC-CRY-5)

### MPE-CRY-040 Production composition gate

MPE shall admit a cryptographic profile to production only after independent review accepts its confidentiality, recognition key hiding, ambiguity handling, nonce lifecycle, replay rules and implemented protocol composition.

- Pattern: ubiquitous
- Scope: PROD
- Priority: MUST
- Source: D1, D3; s2 R1 D9/D10; s1 R2 D1; s4 R2 D1; `2001-bellare-keyprivacy`, abstract; `2022-grubbs-anonrobustpq`, §1.
- Rationale: AEAD confidentiality, KEM security and session-protocol evidence do not independently prove the complete MPE wrapper.
- Verify: inspection, the review covers exact profile bytes and vectors, with no unresolved critical or high findings under its stated severity rubric.
- Status: settled

## Decisions

### DEC-CRY-1 — Prototype security profile and forward secrecy

**Options and proponents**

- Symmetric stream capabilities or static-recipient encryption with no launch forward secrecy: g1, g2, g4; g3 supports one-shot encryption with optional sessions.
- Ratcheted sessions as the launch baseline: s2 and s3; s1 and s4 require an established session protocol inside a reviewed wrapper.
- Epoch hash progression for shared streams: o3 R1; s2 R2 objects that retained keys and recorded initial-key delivery limit the claimed secrecy.

**Recommended default:** The Prototype uses MPE-CRY-001 and reports no content forward secrecy. An optional production pairwise profile follows MPE-CRY-028 through MPE-CRY-035. No session-security claim is attached to Tag rotation.

**Reason:** This gives the Prototype a concrete one-to-many path without silently promising ratchet composition, recovery or historical-key erasure. It preserves s2’s stronger profile as a distinct target. Symmetric rekeying after removal uses independent randomness; hashing a compromised secret does not revoke its holder.

**Settling check:** Compare the profiles under identical workloads, including broadcast fan-out, offline recovery, crash restoration and retained-key compromise. Adopt mandatory ratcheting only after composition review and the PRF/VER acceptance gates succeed.

### DEC-CRY-2 — Tags and recognition

**Options and proponents**

- Complete ciphertext trial opening without Tags: g1, g3, g4; o3 R2 adopts this and withdraws sequence-lookahead Tags.
- Bounded encrypted-header trials: s2 and s3. s2 R2 corrects its attribution: cross-session association is an MPE extension, not specified by Double Ratchet.
- Per-publisher sequence-derived PRF Tags: o1 and o3 R1.
- Hourly broadcast Tags: o4 R1.
- Salted PRF recognition hints: s4 R1.

**Recommended default:** Use the salted Tag construction in MPE-CRY-013, with local bounded recognition and complete Event authentication. The salt is independent of publisher sequence. The default Tag width is P-CRY-2.

**Reason:** A Publisher can abandon sequence numbers without making later Events unrecognizable. Hourly repeated Tags visibly group traffic; sequence lookahead requires recovery beyond its window. Salted recognition remains a new composition assumption requiring review, rather than an inherited anonymity theorem.

**Settling check:** Evaluate the salted profile against no-Tag trial opening and encrypted-header trials. Check arbitrary sequence gaps, rotation, ambiguous opening, adversarial probes, key exposure and maximum-key CPU cost. Remove Tags if their measured benefit does not justify the wrapper and wire overhead.

### DEC-CRY-3 — Invitation and first-contact boundary

**Options and proponents**

- Authenticated invitations with no unsolicited launch contact: s1, s2, s3, s4; o4 R2 accepts this as an abuse-control option.
- Public encryption-key or inbox discovery: g1, g2, o1 and o3 R1.
- FMD-assisted inbox discovery: o1; o2 proposes broader delegated detection.

**Recommended default:** Private subscriptions require authenticated invitations. Public first contact is an optional feature beyond the default profile.

**Reason:** A public recipient key authorizes neither the sender nor unsolicited contact. Confidential transport of an invitation must be distinguished from authentication of its source.

**Settling check:** Demonstrate invitation tamper rejection, publisher-key pinning, recipient consent enforcement, replay handling and bounded first-contact abuse before enabling a public inbox.

### DEC-CRY-4 — Post-quantum posture and sizing

**Options and proponents**

- Classical launch encryption with later crypto agility: g1, g2, g3, g4, o1, o2, o3.
- Hybrid PQXDH establishment with classical ratcheting: s2.
- Future continuous PQ ratcheting or PQ signatures: s2’s later candidates, separately costed.

**Recommended default:** The Prototype’s default remains classical. The production hybrid candidate uses X25519 with ML-KEM-768 and requires one-time prekeys. It does not silently select classical setup or last-resort prekeys.

The checked primitive sizes are:

| Primitive component | Size | Evidence |
|---|---:|---|
| ML-KEM-768 encapsulation key | 1,184 bytes | `2024-nist-fips203`, Table 3 |
| ML-KEM-768 decapsulation key | 2,400 bytes | Same |
| ML-KEM-768 ciphertext | 1,088 bytes | Same |
| ML-KEM-768 shared secret | 32 bytes | Same |
| Plain Ed25519 public key | 32 bytes | `minokawa-compact/doc/api/CompactStandardLibrary/exports.md:109` |
| Plain Ed25519 signature | 64 bytes | Same, `:106` |
| ML-DSA-65 public key | 1,952 bytes | `2024-nist-fips204`, Table 2 |
| ML-DSA-65 signature | 3,309 bytes | Same |

**Reason:** These sizes constrain setup and future signature profiles; they do not determine usable Envelope capacity. PQXDH revision 3 remains classically authenticated (`2023-signal-pqxdh-spec`, §4.1). Midnight’s inspected proof implementation uses KZG commitments and BLS12-381 (`midnight-zk/README.md:12–13`), so hybrid Event setup does not establish whole-system post-quantum security.

**Settling check:** Review the exact ML-KEM/PQXDH adaptation, wrapping and header initialization. Measure complete bootstrap and ordinary Envelope sizes. Any PQ-signature adoption requires a new measured profile and FMT class accounting; signatures must not be truncated to fit.

### DEC-CRY-5 — Fuzzy first-contact detection

**Options and proponents**

- No launch FMD: g1, g3, g4, s2 and o3.
- First-contact-only FMD: o1.
- S-FMD as a mobile subscription mechanism: o2.
- Later FMD evaluation: o4.

**Recommended default:** Disabled. If implemented experimentally, delegate only first-contact detection and authenticate every returned candidate locally. P-CRY-8 applies to the named FMD2 experiment, not automatically to S-FMD.

**Reason:** Detection keys intentionally identify a candidate subset. False positives do not prove relationship privacy; Seres identifies graph-recovery and temporal attacks under its assumptions (`2021-seres-fmdfalsepositives`, §§1, 4–6). Penumbra’s S-FMD selects precision according to global traffic, rather than validating a universal privacy floor (`2022-penumbra-fmd-spec`, “Sender and Receiver FMD”).

Beck’s FMD2 benchmark reports a 68-byte clue, 1.927-millisecond generation and 0.548-millisecond testing at \(p=2^{-5}\) (`2021-beck-fmd`, §7, Table 1). These are literature measurements. Arbitrary random filler is not established as indistinguishable from a valid clue.

**Settling check:** Select the exact construction and codec; measure local costs, false-positive frequency, true-match failures, detector correlations and malformed-clue behavior. PRV must accept the resulting leakage before production activation.

### DEC-CRY-6 — Publisher authentication algorithm

**Options and proponents**

- Ed25519 publisher statements: s2 and g1.
- JubJub Schnorr for contract-oriented authentication: o1, o3 and o4.
- Session-native group authentication: o1 and the MLS proposals.
- Anonymous publication without a named publisher signature: o1.

**Recommended default:** Plain Ed25519 statements with pinned authorized keys. Anonymous publication requires a separately identified policy and does not satisfy authenticated-publisher delivery.

**Reason:** The inspected Compact API supports plain Ed25519 with explicit assertion of the verification result (`minokawa-compact/doc/api/CompactStandardLibrary/exports.md:993–1008`). Its circuit cost relative to JubJub is **unknown**.

**Settling check:** Compile identical authorization fixtures for both algorithms. Measure proving cost and serialized statement sizes, and verify that rejected signatures cannot produce contract effects.

## Cross-area dependencies

These are **expected merge IDs**, not claims that another author has already assigned them. The merge must reconcile their numbering.

| Expected requirement IDs | Required interface or constraint |
|---|---|
| MPE-FMT-001, MPE-FMT-002 | Canonical pre-seal-header bytes, sealed-field encoding, authenticated padding, exact class capacities and profile identifiers |
| MPE-FMT-003 | Separate admission content commitment from the final wire identifier; define proof-dependent exclusions without circularity |
| MPE-PUB-001, MPE-PUB-002 | Complete-Shard reception and back-fill; recognition outcomes do not automatically change retrieval or produce acknowledgements |
| MPE-PUB-003 | Authorized key-generation cutover, recipient exclusion and authenticated re-invitation after revocation |
| MPE-STO-001, MPE-STO-002 | Durable key/replay-state storage and a replay horizon covering authenticated Event validity |
| MPE-CON-001, MPE-CON-002 | Contract constraints bind authenticated statement bytes, destination, action, expiry and secret-bearing consumption nullifier |
| MPE-CON-003 | Contract effect and nullifier insertion occur atomically; publisher authentication remains separate from Anchor inclusion and source-contract provenance |
| MPE-ECO-001 | Admission Proof binds the content commitment; admission membership does not substitute for publisher authentication |
| MPE-NET-001 | GossipSub StrictNoSign policy: absent author, sequence, signature and key fields; rust-libp2p provides this through anonymous publication and validation (`rust-libp2p/protocols/gossipsub/src/behaviour.rs:3105`, `config.rs:46`) |
| MPE-PRV-001, MPE-PRV-002 | Profile leakage definitions, conditional interest-hiding claims and explicit timing, relationship and global-observer non-claims |
| MPE-PRF-001 | Recognition, signature, setup and fan-out budgets for named workloads and client classes |
| MPE-SEC-001, MPE-OPS-001 | Compromise response, trusted key replacement, operator-key separation and profile revocation |
| MPE-VER-001, MPE-VER-002 | Independent vectors, composition review, crash/replay tests and compiled contract-authorization fixtures |

## Glossary additions

| Term | Meaning |
|---|---|
| Cryptographic profile | Versioned specification of algorithms, encodings, domains, key lifecycle and capability claims |
| Private stream | Application-level Event channel identified and authorized inside sealed client state, distinct from a Shard |
| Stream secret | Random capability from which a symmetric stream’s recognition and encryption keys are derived |
| Recognition key | Secret used locally to identify candidate Envelopes; it does not establish publisher authority |
| Envelope salt | Public random input separating recognition or encryption computations between Envelopes |
| Pre-seal header | Canonical immutable public context available before signing and encryption; excludes admission fields dependent on ciphertext |
| Logical identifier | Authenticated Event identity preserved across independently encrypted retries |
| Admission content commitment | Domain-separated commitment to the protected content used as the Admission Proof’s binding input |
| Invitation | Authenticated transfer of subscription authorization and key-establishment material |
| One-time prekey | Setup key whose private material is consumed by one authenticated establishment |
| Skipped-message key | Retained ratchet message key permitting bounded out-of-order opening |
| FMD | Fuzzy message detection, returning candidates that include intended matches and unrelated false positives |
| FMD2 | Beck et al.’s named CCA-secure restricted-probability construction |
| S-FMD | Sender-selected fuzzy detection precision, as described by Penumbra |
| Consumption nullifier | Destination-scoped replay value derived from an Event-specific secret |
| Forward secrecy | Conditional protection of earlier content after later compromise, subject to erasure and retained-key exclusions |
| Post-compromise recovery | Restoration of session confidentiality following fresh uncompromised contributions under the selected protocol’s conditions |

## Gaps

- **Formal consensus is unknown.** “Settled” identifies requirements without a material competing obligation in the reviewed material; it does not certify the charter’s Round 3 voting threshold. Open defaults require merge review.
- **Salted Tag composition is unproved.** Its exact encoding, key schedule and multi-key behavior require independent analysis. Primitive PRF security does not establish MPE relationship privacy.
- **Session association remains an extension.** Double Ratchet specifies header-key trials within an associated session. Cross-session recognition and its interaction with Tags require separate vectors and review.
- **Group session security is incomplete.** Shared symmetric streams provide reading capabilities and separately signed authorship. They do not implement MLS membership agreement or group recovery. Any MLS profile must protect its complete framing; RFC 9420 §6.3 exposes group and epoch fields.
- **Erasure below the application boundary is unknown.** Swap, backups, crash dumps and storage media may retain secrets. MPE-CRY-029 establishes application-state erasure; a stronger deployment guarantee needs an independently verified storage policy.
- **PQ composition and complete sizes are unknown.** The supplied PQXDH revision predates standardized ML-KEM. Primitive sizes are checked; final setup capacity, wrapping overhead and proving cost remain measurements required by MPE-CRY-036.
- **FMD privacy acceptance criteria are unresolved.** No universal false-positive rate establishes the brief’s interest-hiding property. A valid-clue versus filler indistinguishability argument is also absent.
- **Cryptographic CPU thresholds belong to PRF.** Recognition and verification costs are unknown for the Prototype’s hardware and workloads; literature microbenchmarks cannot supply acceptance thresholds.
- **Replay lifetime needs PUB/STO agreement.** Durable replay records must cover authenticated validity. GossipSub’s seen cache alone is not an application replay policy.
- **Midnight activation is unknown.** Checked Compact documentation establishes signature API behavior, not availability of every API on the deployment target.
- **Franking remains unspecified.** A reserved commitment slot does not implement verifiable abuse reporting. The exact report protocol, opening rules and recipient/sender capabilities need a separate reviewed design.