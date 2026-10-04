# Message journey: proposed interaction copy

Use nine selectable steps. Steps 1–4 form the publication path; after distribution, retention, reception and anchoring proceed independently. The numbered interaction is an explanatory tour, not a claim that these operations occur in this exact order. Ordinary coordination can complete locally without an on-chain effect.

Intro: **Follow a private event from signed intent to an explicit business outcome.** Delivery, retention, ledger inclusion and business completion each provide different evidence.

| Step | Label | Short copy | Expanded explanation |
|---|---|---|---|
| 1 | Define the intent | The application creates a typed event and signs its business intent. | A CloudEvents-compatible payload carries event identity, source, type and schema inside encryption. Application policy defines roles, allowed actions and expiry. A business signature establishes the claimed authority; transport security alone does not authorize an effect. |
| 2 | Seal the envelope | MPE encrypts the event and prepares keyed local recognition. | Fixed envelope classes, AEAD and publisher signatures preserve the selected MPE profile. Semantic metadata stays encrypted. The salt, nonce and recognition tag are readable prefix fields, and matching remains local and keyed. Launch streams use the original symmetric profile; OpenMLS is a separately gated extension. |
| 3 | Prove admission | One anonymous proof binds membership and allowance to this envelope. | The selected RLN-style relation uses finalized Midnight Registry roots and binds the admission context, size class, credit and envelope identity. Semaphore-derived patterns support identity and witness lifecycle; there is no second membership proof per event. This admission proves permission to publish, not business authority. |
| 4 | Distribute | GossipSub carries opaque envelopes across the overlay. | The default private profile uses whole-shard distribution without business topics or content-aware routing. Expiry must be checked on cached and queued sends too. Static launch streams do not claim forward secrecy or ingress anonymity. |
| 5 | Retain and recover | Stores persist opaque envelopes and issue signed retention evidence. | The custom MPE store protocol supplies replica selection, receipt-after-persistence, whole-window backfill, pruning and explicit gaps. A database alone does not implement this protocol. A signed persistence receipt is evidence of its stated retention commitment; it does not establish anchor inclusion, receiver processing or business completion. |
| 6 | Recognize locally | The receiver scans its shard and opens matching events locally. | Recognition stays inside the endpoint trust domain. Reception and recovery must not introduce recognition-triggered upstream selectors. Authentication and application policy govern whether a recognized event may enter processing. Private mobile discovery and retrieval remain a separate research gate. |
| 7 | Commit local processing | The endpoint durably records the event and commits recoverable workflow progress. | Use a durable inbox and an atomic local effect / dedup / outbox / checkpoint / cursor composition. Trusted Node backend hosts select UmbraDB with PostgreSQL; standalone Rust nodes and clients select SQLite. UmbraDB's proposed MPE capability remains a gate: current saveAndAdvance covers checkpoint/cursor only. External effects need destination idempotency or reconciliation. A local commit establishes local processing progress, not automatic business acknowledgement. |
| 8 | Establish ledger evidence | Window commitments can establish finalized anchor inclusion. | Anchoring is a parallel branch from distribution, not a prerequisite for every local notification. Inclusion establishes that the committed envelope belongs to the anchored window. For a requested contract effect, the consumer must also prove signed authority, replay protection and anchored-message binding; the contract verifies the proof and atomically commits the effect. A carried contract event additionally requires exact bytes and applied-phase checks. Inclusion alone authorizes no effect. |
| 9 | Acknowledge the outcome | The application explicitly signs the business result. | When its workflow policy requires confirmation, the endpoint issues a signed business acknowledgement after the relevant local processing or authorized contract result. Publish that acknowledgement as its own event through the same envelope and admission path. Receipt, recognition, local commit and anchor inclusion never automatically mean that the recipient accepted an offer, posted a payment or approved an action. |

## Flow wiring

```text
Application → Signed intent → MPE sealing → Anonymous admission → GossipSub
                                                               ├→ Opaque stores → Persistence receipts / whole-window backfill
                                                               ├→ Whole-shard receiver → Local recognition → Durable inbox
                                                               │                                              ↓
                                                               │                       Policy → Atomic local commit
                                                               │                                              ↓
                                                               │                         Explicit business acknowledgement
                                                               └→ Window anchor → Finalized inclusion

Optional contract effect:
Authenticated workflow + signed authority + replay/message binding + anchor evidence
  → Consumer proof → Contract verification and atomic effect
  → Explicit business acknowledgement when required by application policy
```

When step 5 is selected, illuminate the store branch and reconnect its backfill arrow to the whole-shard receiver. When step 8 is selected, illuminate the anchor branch and optional consumer-proof route. Keep step 9 visibly controlled by application policy. Acknowledgements are new signed events, not automatic network-generated confirmations.

## Distinct evidence labels

| Evidence | What it establishes | What remains separate |
|---|---|---|
| Admission accepted | Publication meets the selected membership/quota relation at validation | Durable storage, inclusion, processing, business outcome |
| Persistence receipt | A store's signed retention commitment issued after persistence | Receiver processing, anchor inclusion, business outcome |
| Local durable commit | The endpoint recorded the specified local workflow progress atomically | External destination reconciliation, inclusion, explicit business outcome |
| Finalized anchor inclusion | The envelope is included in a finalized window commitment | Business authority, replay protection and contract-effect binding |
| Explicit business acknowledgement | A signer asserts the application-defined outcome | Independent verification of authority and any referenced external/ledger result |

Footer caveat: **Recommended architecture; design and exploratory stage.** Dependency selection is not implementation acceptance. Production admission, durable replication, the UmbraDB MPE composition, authorized ledger effects, OpenMLS and private mobile reception retain their separate validation gates.

Sources: docs/product-requirements/recommended-stack-and-use-cases.md; docs/product-requirements/requirements-fit-and-open-source.md.
