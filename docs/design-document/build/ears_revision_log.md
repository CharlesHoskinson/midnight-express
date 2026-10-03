# Requirement register: amendment log (owner only, not part of the document)

Compiled from `ears_revisions.json` and the outputs of `ears_consolidate.py` (revisions plus the vocabulary pass). Sources: `align/FOUNDATION_DEFINITIONS.md` (7.5 items 26-41, 7.1 items 2-4, 6.4/6.5, 5.2 where noted), `align/GOSSIPSUB_COMPLIANCE.md` section 4 (cN = correction N), `prototype/registry/RESULTS.md` section 6.

## Counts

| | Before | After |
|---|---|---|
| total | 572 | 616 |
| dup | 114 | 114 |
| withdrawn | 2 | 2 |
| poc | 322 | 335 |
| prod | 134 | 165 |
| open | 155 | 169 |
| must | 399 | 437 |
| should | 46 | 47 |
| may | 11 | 16 |
| live (poc + prod) | 456 | 500 |
| FMT | 53 | 59 |
| CRY | 41 | 46 |
| PUB | 53 | 53 |
| CON | 57 | 63 |
| ECO | 53 | 57 |
| NET | 56 | 70 |
| PRF | 41 | 43 |
| STO | 42 | 42 |
| OPS | 55 | 56 |
| PRV | 38 | 44 |
| SEC | 42 | 42 |
| VER | 41 | 41 |

Operations: 78 records replaced, 44 added, 3 parameter meanings changed (P-FMT-8, P-FMT-10, P-FMT-11).

## Records replaced or added

| Record | Op | Reason |
|---|---|---|
| MPE-FMT-010 | replace | GossipSub c16: the 65,536 B cap is an encoded-RPC limit, separate from the Envelope length check. (same-obligation entry; text kept consistent, still a pointer) |
| MPE-FMT-018 | replace | Foundation 7.5 #30: domain string moved to the `mpe:<purpose>[v1]` convention (P-FMT-11 = `mpe:envelope-id[v1]`). |
| MPE-FMT-019 | replace | GossipSub c4: the message id is the full-byte hash of NET-010, not the Envelope Identifier (was wrong). (same-obligation entry; text kept consistent, still a pointer) |
| MPE-FMT-023 | replace | GossipSub c8: Reject only for a version mismatch under a supported GossipSub topic; unsupported context goes to SEC-008 (Ignore). |
| MPE-FMT-032 | replace | GossipSub c19: covers queued sends; stock IWANT caches ignore MPE expiry, so a conformance test per implementation is required. |
| MPE-FMT-040 | replace | Foundation 7.5 #26 (MIP-0018 naming): `mip-xxxx:envelope[v1]`, NUL-padded; status settled because the convention is fixed. |
| MPE-FMT-042 | replace | Registry results 6 / limitation 16: 'guaranteed phase' replaced by 'one execution phase of one intent' (MIP-0019). |
| MPE-FMT-043 | replace | Foundation 7.5 #28: 288 bytes is `Misc` struct data, not serialized size; serialized size measured under PRF-040. |
| MPE-FMT-044 | replace | Registry results 6: keeps 16 parts as the fee limit and states the proving cost (k = 22 for 16 parts, k = 20 for 4). |
| MPE-FMT-047 | replace | Foundation 7.5 #26: Anchor `Misc` named `mip-xxxx:anchor[v1]`; payload is the NET-050 layout; Anchors verified against state, not the event. |
| MPE-FMT-053 | replace | Foundation 7.5 #33 (MIP-0012 suite byte): one-byte suite identifier added to the profile binding; now open (location in the layout not yet fixed). |
| MPE-FMT-054 | add | Foundation 7.5 #36 / 6.4: reserved schema identifier for carried events. |
| MPE-FMT-055 | add | Foundation 7.5 #36 / 6.4 #1, #6: verbatim `VersionedLogItem` bytes, no re-typing. |
| MPE-FMT-056 | add | Foundation 7.5 #36 / 6.5: transaction hash and position carried with the event. |
| MPE-FMT-057 | add | Foundation 5.2 #1: carried events decoded only with Midnight's decoder. |
| MPE-FMT-058 | add | Foundation 7.5 #36 / 5.2 #2: `@topic` values of a carried private event stay inside the Sealed Body. |
| MPE-FMT-059 | add | Registry results 6 (circuit encoding rule): non-constant emitted bytes bounded (72 B Anchor, 35 B governance). |
| MPE-CRY-001 | replace | Foundation 7.5 #33: default profile is suite 0x01. |
| MPE-CRY-006 | replace | Foundation 7.5 #30 (MPS-0027): every label in the `mpe:<purpose>[v<n>]` form. |
| MPE-CRY-020 | replace | Foundation 7.5 #34: Ed25519 vs JubJub Schnorr decided by circuit measurement; decision now DEC-022. |
| MPE-CRY-027 | replace | Foundation 7.5 #32 (MIP-0015): admission secret and invitation keys may come from `deriveSecret` with fixed domains. |
| MPE-CRY-041 | replace | Foundation 7.5 #34: signature field is the suite's algorithm (64 B for Ed25519). |
| MPE-CRY-042 | add | Foundation 7.5 #30: publish the label table for MPS-0027 registration. |
| MPE-CRY-043 | add | Foundation 7.5 #34: optional JubJub Schnorr publisher profile (`jubjubSchnorrVerify`). |
| MPE-CRY-044 | add | Foundation 7.5 #33 / 5.2 #3: no frozen shielded-key suite before MPS-0005 Part 2 defines `encrypt_for`. |
| MPE-CRY-045 | add | Foundation 7.5 #33: deferred first-contact profile to Midnight shielded encryption keys (MIP-0007 resolution), off by default. |
| MPE-CRY-046 | add | Registry results 6 (circuit encoding rule) / limitation 13: struct preimages for in-circuit hashes. |
| MPE-PUB-009 | replace | Foundation 7.5 #40: note that MPS-0005's indexer relevance model is excluded by design. |
| MPE-PUB-010 | replace | Foundation 7.5 #40: same note. |
| MPE-PUB-015 | replace | GossipSub c22: repair fetches complete differing windows, never per-identifier selections. |
| MPE-PUB-022 | replace | GossipSub c22: `accepted` follows the ingress `Accepted` reply (application acceptance), not a GossipSub outcome. |
| MPE-PUB-026 | replace | GossipSub c4: sentence wrongly equated the message id with the Envelope identifier; now points to NET-010. (same-obligation entry; text kept consistent, still a pointer) |
| MPE-PUB-043 | replace | Foundation 7.5 #39: ledger-lane cursor is the Indexer `id` translated by the Ledger Adapter. |
| MPE-PUB-051 | replace | GossipSub c6: it is the payload that waits for validation. (same-obligation entry; text kept consistent, still a pointer) |
| MPE-CON-016 | replace | Foundation 7.5 #31 (merged with SEC-022): Anchors verified against Bus Registry state; lane parts against P-NET-14 sources or replay. |
| MPE-CON-026 | replace | GossipSub c22: `accepted` no longer claims that a mesh peer holds the Envelope. |
| MPE-CON-043 | replace | Foundation 7.5 #34 + Registry results (DEC-022): signature under the suite's algorithm; both algorithms measured. |
| MPE-CON-046 | replace | Registry results 6: expiry may come from the anchored creation minute. |
| MPE-CON-047 | replace | Registry results 6: Anchor tree (HistoricMerkleTree<12>, slot window mod 2940), witness-free Registry check, two calls. |
| MPE-CON-053 | replace | Foundation 7.5 #39: resumes from the Indexer `id` translated by the Ledger Adapter; 'fallback' renamed ledger lane. |
| MPE-CON-058 | add | Foundation 7.5 #36 / 6.4 #5: carried event stays `gossip` until transcript match in a finalized block. |
| MPE-CON-059 | add | Foundation 7.5 #36 / 6.4 #5 (MIP-0019): fallible-phase success check. |
| MPE-CON-060 | add | Registry results 6 (consumer authority) / limitation 12: inclusion alone gives no authority; signature binds nullifier to Message. |
| MPE-CON-061 | add | Registry results 6 / limitation 5: only a coarse prover-chosen time bound is disclosed. |
| MPE-CON-062 | add | Foundation 7.5 #38 (MPS-0028): deferred `in-block` label. |
| MPE-CON-063 | add | Foundation 7.5 #38 (MIP-0018 6.2): rollback of `in-block` on reorganization. |
| MPE-ECO-004 | replace | Registry results 6 / limitation 11: a contract cannot check a DUST payment; registration is a transaction, fee is the network fee. |
| MPE-ECO-006 | replace | Foundation 7.5 #32: admission secret may come from `deriveSecret` (CRY-027), still independent of wallet keys. |
| MPE-ECO-011 | replace | Foundation 7.5 #29: budget covers `bytes_written` and ledger-lane parts. |
| MPE-ECO-015 | replace | Registry results 6 / limitation 7: the root window is enforced by Bus Nodes only (verification line). |
| MPE-ECO-022 | replace | GossipSub c24: no network-wide quota follows from mesh connectivity; per-node bound with conflict evidence. |
| MPE-ECO-026 | replace | Registry results 6: one membership tree per period (pruning split out to ECO-055). |
| MPE-ECO-027 | replace | Registry results 6 / limitations 4, 6: root times come from block timestamps via the Ledger Adapter (system changed). |
| MPE-ECO-028 | replace | Registry results 6: evidence check specified (two shares on one line, distinct EIDs, Merkle path). |
| MPE-ECO-032 | replace | Foundation 7.5 #41: note that bonds are contract balances unrelated to NIGHT staking (covers ECO-032 to 042). |
| MPE-ECO-049 | replace | Registry results 6: measured model inputs replace the 8,192-byte assumption until devnet figures exist. |
| MPE-ECO-054 | add | Foundation 7.5 #35: admission secret never sent to an unattested prover. |
| MPE-ECO-055 | add | Registry results 6: permissionless pruning of a period tree one root window after the period. |
| MPE-ECO-056 | add | Registry results 6 (registration price instrument). |
| MPE-ECO-057 | add | Registry results 6 (protocol hash for RLN) / limitation 15: no `transientHash` in the admission relation. |
| MPE-NET-006 | replace | GossipSub c2 + c17: `/mpe/<g>/1` naming; the 8-byte prefix is a routing label, admission binds the full genesis hash. |
| MPE-NET-008 | replace | GossipSub c1: profile is v1.1 scoring plus v1.2 IDONTWANT; v1.2 spec status noted. |
| MPE-NET-009 | replace | GossipSub c3: empty fields count; penalty on the forwarding peer; pinned 0.50.0 decoder lacks the `key` check. |
| MPE-NET-010 | replace | GossipSub c4 + Foundation #30: exact hash input (`Message.data`, framing excluded); label `mpe:msgid[v1]`. |
| MPE-NET-011 | replace | GossipSub c13: v1.1 mesh constraints in the sentence; Go validator mismatch recorded; maintenance bounds are not guarantees. |
| MPE-NET-014 | replace | GossipSub c16: the cap applies to the encoded RPC including batching and control fields. |
| MPE-NET-015 | replace | GossipSub c6: payload forwarding waits for Accept; listed pre-validation work is permitted. |
| MPE-NET-022 | replace | GossipSub c11: verification covers asymmetric topologies and first-delivery approximation. |
| MPE-NET-024 | replace | GossipSub c18: `prune_peers` above zero; reference bootstrappers relay until demonstrated. |
| MPE-NET-027 | replace | GossipSub c18: PX suggestions also checked against Bus Registry authorization. |
| MPE-NET-028 | replace | GossipSub c18: every dial source passes the same authentication and address checks. |
| MPE-NET-034 | replace | GossipSub c10 (table row): exclusion must not rely on the -20 P5 score alone. (same-obligation entry; text kept consistent, still a pointer) |
| MPE-NET-040 | replace | Foundation 7.5 #26 + Registry results 6: Bus Registry emits only `mip-xxxx:anchor[v1]` / `mip-xxxx:governance[v1]` `Misc`; open (Paused/Unpaused vs Misc). |
| MPE-NET-044 | replace | Foundation 7.5 #26, #27: contradiction with FMT-041 removed (4^c parts, not one `Misc`). |
| MPE-NET-047 | replace | GossipSub c15: on/off experiments state which IDONTWANT behaviour is disabled. |
| MPE-NET-048 | replace | GossipSub c22: whole-Shard feed is an MPE service, not a GossipSub subscription. |
| MPE-NET-049 | replace | GossipSub c22: `Accepted` means committed application acceptance; Busy/Refused are service replies. |
| MPE-NET-050 | replace | Registry results 6: fixed 256-byte payload (u64 BE window, root, 8 x u32 BE counts, zero fill). |
| MPE-NET-053 | replace | Registry results 6 / limitation 3: anchorer proves preimage of a stored key commitment (no signer). |
| MPE-NET-054 | replace | Registry results 6 + GossipSub c20: relay key = SHA-256 of the PeerId; anchorer key commitment added. |
| MPE-NET-055 | replace | Registry results 6: root times from including block timestamps. |
| MPE-NET-057 | add | GossipSub c2: record negotiated protocol and peer kind. |
| MPE-NET-058 | add | GossipSub c2: enforce the selected v1.2 version policy. |
| MPE-NET-059 | add | GossipSub c6: local publications pass the same validation before `publish`. |
| MPE-NET-060 | add | GossipSub c6: validation result reported within the message-cache lifetime; failure is not propagation. |
| MPE-NET-061 | add | GossipSub c22: publish enqueue failures reported separately. |
| MPE-NET-062 | add | GossipSub c15: IDONTWANT on negotiated v1.2 links. |
| MPE-NET-063 | add | GossipSub c15: Rust threshold predicate (serialized length, strict >). |
| MPE-NET-064 | add | GossipSub c15: no penalty for sends despite IDONTWANT. |
| MPE-NET-065 | add | GossipSub c15: per-heartbeat IDONTWANT limit before any excess penalty. |
| MPE-NET-066 | add | GossipSub c17: subscription name filter (default allow-all filter is insufficient). |
| MPE-NET-067 | add | GossipSub c17: partial messages and other extensions outside the launch profile. |
| MPE-NET-068 | add | Foundation 7.5 #38: Ledger Adapter never takes values from unfinalized blocks. |
| MPE-NET-069 | add | Registry results 6 (clock tolerance) / limitation 4: 900 s tolerance on caller clock values. |
| MPE-NET-070 | add | Registry results 6 (Registry toolchain): Compact 0.33.0 or later for `emit` and witness-free cross-contract reads. |
| MPE-PRF-010 | replace | GossipSub c1 + c13: benchmark the v1.2 profile; tuples satisfy NET-011 constraints. |
| MPE-PRF-018 | replace | Foundation 5.2 #13: state per hardware class whether admission proving runs locally. |
| MPE-PRF-040 | replace | Foundation 7.5 #28, #29: ceiling under `block_usage` and `bytes_written`, measured `Misc` sizes. |
| MPE-PRF-042 | add | Registry results 6 (proving budget): circuit sizes stated in the MIP. |
| MPE-PRF-043 | add | Registry results 6 (proving budget): Anchor proving must fit one window. |
| MPE-STO-013 | replace | GossipSub c25: lifetime is expiry plus P-FMT-4 (P-STO-6 no longer referenced), independent of the transport seen cache. (same-obligation entry; text kept consistent, still a pointer) |
| MPE-STO-028 | replace | Registry results 6 / limitation 9: 2,940-slot ring indexed by window mod 2940. |
| MPE-STO-029 | replace | Registry results 6: pruning is permissionless. |
| MPE-OPS-004 | replace | GossipSub c18: no signed-record PX claim for the reference; addresses from Bus Registry and bootstrap records. (same-obligation entry; text kept consistent, still a pointer) |
| MPE-OPS-018 | replace | Registry results 6 + Foundation #26: governance `Misc` `mip-xxxx:governance[v1]` with action/reason/subject payload; open. |
| MPE-OPS-044 | replace | Registry results 6: confirmed by compilation (toolchain floor only for `emit`). |
| MPE-OPS-046 | replace | Registry results 6: measured model inputs until devnet figures exist. (same-obligation entry; text kept consistent, still a pointer) |
| MPE-OPS-056 | add | Registry results 6 (Registry toolchain) + Foundation 5.2 #7: MIP names toolchain, language, runtime and ledger versions. |
| MPE-PRV-007 | replace | Foundation 7.5 #40: relevance-model note. |
| MPE-PRV-008 | replace | Foundation 7.5 #40: relevance-model note. (same-obligation entry; text kept consistent, still a pointer) |
| MPE-PRV-039 | add | Foundation 7.5 #37 (MPS-0043): per-Message disclosure object with discloser signature. |
| MPE-PRV-040 | add | Foundation 7.5 #37: per-period disclosure object. |
| MPE-PRV-041 | add | Foundation 7.5 #37: disclosures verified against Anchors. |
| MPE-PRV-042 | add | Foundation 7.5 #37: stated disclosure lifetime. |
| MPE-PRV-043 | add | Foundation 7.5 #37 + 7.2 #14: mapping to MPS-0043 goals 1-5; stream secret is a coarse irrevocable viewing capability. |
| MPE-PRV-044 | add | GossipSub c20: Identify fields declared as permitted leakage when enabled. |
| MPE-SEC-004 | replace | GossipSub c1: scoring profile is the v1.1 rules within the v1.2 profile. (same-obligation entry; text kept consistent, still a pointer) |
| MPE-SEC-005 | replace | GossipSub c6: payload forwarding waits for admission validation. |
| MPE-SEC-008 | replace | GossipSub c8: 'unsupported version' narrowed to unsupported protocol context. (same-obligation entry; text kept consistent, still a pointer) |
| MPE-SEC-022 | replace | Foundation 7.5 #31 (merged with CON-016): `final` labelling also requires confirmed state. |
| MPE-VER-011 | replace | GossipSub c1: demonstration under the v1.2 profile. |
| MPE-VER-030 | replace | Registry results 6: measured model inputs until devnet figures exist. |

## Parameter meanings changed

- P-FMT-8: 16 parts kept as the fee limit; proving cost stated (Registry results 6).
- P-FMT-10: `mip-xxxx:anchor[v1]`, `mip-xxxx:envelope[v1]`, `mip-xxxx:governance[v1]`, NUL-padded (Foundation #26).
- P-FMT-11: `mpe:envelope-id[v1]` (Foundation #30).

## Vocabulary-only changes

304 further records changed only through the vocabulary pass (STYLE.md 'Vocabulary'); listed by rule (a record can appear under several rules).

- **topic -> stream or GossipSub topic** (18): MPE-CON-001, MPE-FMT-004, MPE-FMT-024, MPE-FMT-052, MPE-NET-013, MPE-NET-031, MPE-NET-032, MPE-NET-043, MPE-PRV-003, MPE-PUB-001, MPE-PUB-006, MPE-PUB-007, MPE-PUB-008, MPE-PUB-017, MPE-PUB-019, MPE-PUB-030, MPE-PUB-039, MPE-PUB-046
- **Envelope -> MPE Envelope (sentences)** (148): MPE-CON-002, MPE-CON-003, MPE-CON-011, MPE-CON-012, MPE-CON-013, MPE-CON-024, MPE-CON-032, MPE-CON-037, MPE-CON-038, MPE-CON-045, MPE-CRY-002, MPE-CRY-003, MPE-CRY-005, MPE-CRY-007, MPE-CRY-012, MPE-CRY-013, MPE-CRY-014, MPE-CRY-017, MPE-CRY-022, MPE-CRY-023, MPE-CRY-028, MPE-CRY-036, MPE-ECO-001, MPE-ECO-012, MPE-ECO-013, MPE-ECO-014, MPE-ECO-016, MPE-ECO-018, MPE-ECO-019, MPE-ECO-020, MPE-ECO-023, MPE-ECO-024, MPE-ECO-025, MPE-ECO-037, MPE-ECO-041, MPE-ECO-044, MPE-ECO-045, MPE-ECO-046, MPE-ECO-051, MPE-FMT-005, MPE-FMT-006, MPE-FMT-007, MPE-FMT-008, MPE-FMT-009, MPE-FMT-012, MPE-FMT-013, MPE-FMT-015, MPE-FMT-016, MPE-FMT-020, MPE-FMT-021, MPE-FMT-024, MPE-FMT-029, MPE-FMT-030, MPE-FMT-031, MPE-FMT-036, MPE-FMT-045, MPE-FMT-049, MPE-FMT-052, MPE-NET-002, MPE-NET-004, MPE-NET-016, MPE-NET-017, MPE-NET-018, MPE-NET-023, MPE-NET-032, MPE-NET-033, MPE-NET-038, MPE-NET-051, MPE-NET-052, MPE-NET-056, MPE-OPS-006, MPE-OPS-021, MPE-OPS-022, MPE-OPS-025, MPE-OPS-026, MPE-OPS-031, MPE-OPS-032, MPE-OPS-035, MPE-OPS-036, MPE-PRF-001, MPE-PRF-002, MPE-PRF-005, MPE-PRF-006, MPE-PRF-007, MPE-PRF-021, MPE-PRF-023, MPE-PRF-032, MPE-PRV-003, MPE-PRV-005, MPE-PRV-010, MPE-PRV-028, MPE-PRV-038, MPE-PUB-001, MPE-PUB-002, MPE-PUB-003, MPE-PUB-005, MPE-PUB-011, MPE-PUB-012, MPE-PUB-013, MPE-PUB-014, MPE-PUB-023, MPE-PUB-027, MPE-PUB-028, MPE-PUB-029, MPE-PUB-031, MPE-PUB-035, MPE-PUB-036, MPE-PUB-042, MPE-PUB-045, MPE-PUB-053, MPE-SEC-006, MPE-SEC-007, MPE-SEC-013, MPE-SEC-014, MPE-SEC-015, MPE-SEC-018, MPE-SEC-019, MPE-SEC-021, MPE-SEC-023, MPE-SEC-025, MPE-SEC-034, MPE-SEC-035, MPE-SEC-041, MPE-SEC-042, MPE-STO-003, MPE-STO-004, MPE-STO-005, MPE-STO-006, MPE-STO-007, MPE-STO-009, MPE-STO-011, MPE-STO-015, MPE-STO-016, MPE-STO-017, MPE-STO-018, MPE-STO-020, MPE-STO-021, MPE-STO-024, MPE-STO-034, MPE-STO-036, MPE-STO-037, MPE-STO-038, MPE-STO-041, MPE-STO-042, MPE-VER-004, MPE-VER-005, MPE-VER-014, MPE-VER-025
- **epoch -> admission window (key epochs -> key period)** (17): MPE-CON-031, MPE-ECO-013, MPE-ECO-014, MPE-ECO-016, MPE-ECO-017, MPE-ECO-021, MPE-ECO-052, MPE-ECO-053, MPE-FMT-005, MPE-PRF-030, MPE-PUB-046, MPE-PUB-053, MPE-SEC-013, MPE-SEC-017, MPE-STO-014, MPE-STO-015, MPE-VER-019
- **Event -> Message (incl. Logical Message Identifier)** (75): MPE-CON-007, MPE-CON-008, MPE-CON-011, MPE-CON-012, MPE-CON-014, MPE-CON-015, MPE-CON-017, MPE-CON-018, MPE-CON-019, MPE-CON-020, MPE-CON-021, MPE-CON-022, MPE-CON-027, MPE-CON-028, MPE-CON-034, MPE-CON-035, MPE-CON-039, MPE-CON-041, MPE-CON-042, MPE-CON-045, MPE-CON-049, MPE-CON-051, MPE-CON-052, MPE-CON-057, MPE-CRY-002, MPE-CRY-013, MPE-CRY-014, MPE-CRY-019, MPE-CRY-022, MPE-CRY-023, MPE-CRY-024, MPE-CRY-025, MPE-CRY-031, MPE-ECO-003, MPE-FMT-014, MPE-FMT-015, MPE-FMT-016, MPE-FMT-017, MPE-FMT-022, MPE-FMT-026, MPE-FMT-034, MPE-FMT-038, MPE-FMT-039, MPE-NET-042, MPE-PRF-001, MPE-PRV-005, MPE-PRV-011, MPE-PRV-014, MPE-PRV-015, MPE-PUB-004, MPE-PUB-019, MPE-PUB-020, MPE-PUB-021, MPE-PUB-037, MPE-PUB-038, MPE-PUB-040, MPE-PUB-044, MPE-PUB-045, MPE-PUB-047, MPE-PUB-048, MPE-PUB-049, MPE-SEC-029, MPE-SEC-032, MPE-SEC-033, MPE-SEC-037, MPE-SEC-038, MPE-STO-001, MPE-STO-012, MPE-STO-023, MPE-VER-008, MPE-VER-023, MPE-VER-024, MPE-VER-029, MPE-VER-032, MPE-VER-036
- **Registry -> Bus Registry** (59): MPE-ECO-005, MPE-ECO-007, MPE-ECO-008, MPE-ECO-024, MPE-ECO-025, MPE-ECO-029, MPE-ECO-030, MPE-ECO-033, MPE-ECO-034, MPE-ECO-035, MPE-ECO-037, MPE-ECO-038, MPE-ECO-039, MPE-ECO-040, MPE-ECO-041, MPE-ECO-042, MPE-FMT-033, MPE-NET-020, MPE-NET-026, MPE-NET-031, MPE-NET-032, MPE-NET-035, MPE-NET-036, MPE-NET-037, MPE-NET-038, MPE-NET-039, MPE-NET-046, MPE-OPS-006, MPE-OPS-007, MPE-OPS-010, MPE-OPS-012, MPE-OPS-013, MPE-OPS-014, MPE-OPS-015, MPE-OPS-016, MPE-OPS-019, MPE-OPS-020, MPE-OPS-021, MPE-OPS-022, MPE-OPS-023, MPE-OPS-027, MPE-OPS-037, MPE-OPS-041, MPE-OPS-048, MPE-OPS-052, MPE-OPS-055, MPE-PUB-002, MPE-PUB-003, MPE-PUB-004, MPE-PUB-034, MPE-SEC-001, MPE-SEC-013, MPE-SEC-035, MPE-STO-001, MPE-STO-016, MPE-STO-040, MPE-VER-010, MPE-VER-034, MPE-VER-039
- **Tag -> Recognition Tag** (13): MPE-CON-001, MPE-CON-007, MPE-CRY-004, MPE-CRY-012, MPE-CRY-013, MPE-CRY-014, MPE-CRY-015, MPE-FMT-051, MPE-NET-043, MPE-PUB-005, MPE-PUB-030, MPE-SEC-025, MPE-SEC-027
- **nullifier qualified** (11): MPE-CON-044, MPE-CON-045, MPE-CRY-025, MPE-ECO-013, MPE-ECO-017, MPE-ECO-018, MPE-ECO-019, MPE-ECO-020, MPE-ECO-021, MPE-ECO-030, MPE-ECO-052
- **Operator -> Bus Operator** (22): MPE-CON-036, MPE-ECO-002, MPE-ECO-037, MPE-ECO-046, MPE-NET-025, MPE-OPS-005, MPE-OPS-006, MPE-OPS-009, MPE-OPS-025, MPE-OPS-034, MPE-OPS-050, MPE-OPS-051, MPE-OPS-055, MPE-PRV-033, MPE-PUB-014, MPE-SEC-002, MPE-SEC-021, MPE-STO-012, MPE-STO-031, MPE-STO-033, MPE-STO-042, MPE-VER-038
- **node -> Store Node / Bus Node** (2): MPE-PRF-005, MPE-PUB-042
- **fallback -> ledger lane / carrier** (5): MPE-CON-019, MPE-CON-050, MPE-NET-042, MPE-PRV-020, MPE-VER-024
- **Phase/phase -> Stage/stage** (13): MPE-NET-002, MPE-OPS-001, MPE-OPS-008, MPE-OPS-017, MPE-OPS-020, MPE-OPS-041, MPE-OPS-042, MPE-OPS-043, MPE-OPS-045, MPE-OPS-049, MPE-OPS-051, MPE-OPS-054, MPE-VER-003
- **bridge -> ledger input / ledger interface** (2): MPE-VER-033, MPE-VER-037

The same pass also ran on the parameter tables, the area scope texts and the withdrawn-entry reasons; the FMT area title became 'Message and MPE Envelope format'; the appendix introduction now names Midnight Express and points to a generated A.0 Glossary.

## Not applied, and why

- GossipSub corrections 5, 7, 9, 12, 14, 21 and 23 name no MPE requirement identifier in their replacement text (they target prose, the prototype notes and the MIP drafts); existing requirements already carry the obligations of 21 (MPE-PUB-012, MPE-SEC-025) and 23 (MPE-SEC-040 / MPE-VER-026 as release gates).
- RESULTS 6 'P-ECO-5': the reconciled parameter row is shared and was not edited; the Bus Node enforcement is stated in MPE-ECO-015's verification line.
- 'gateway fallback', 'Indexer fallback' and the generic 'privacy-changing fallback' (MPE-NET-043, MPE-PRF-039, MPE-PRV-013, MPE-SEC-026) do not name the ledger lane and keep the word.

## Pre-existing defect noticed (not changed)

- Split fixes in `design/ears/reconcile.json` (ids like MPE-FMT-001a / 001b) are parsed by `lint.records` as the same id, so the 'b' record overwrites the 'a' record and the title keeps a stray 'a '/'b ' prefix (e.g. 'MPE-FMT-001 b No variable encodings...'). Affected: MPE-CON-005, MPE-CON-025, MPE-CON-044, MPE-FMT-001, MPE-NET-001, MPE-NET-009, MPE-NET-043, MPE-OPS-033. Fixing it changes the counts, so it was left for a separate decision.

