# Midnight Express

A private event delivery system for the [Midnight](https://midnight.network) network, built on
[GossipSub](https://github.com/libp2p/specs/tree/master/pubsub/gossipsub) with ledger anchoring.

Midnight Express carries confidential messages between agents, smart contracts and wallets without
showing the infrastructure what the messages say, who is waiting for them, or how the parties relate.
It is designed as a complement to on-chain private events, and, under stated conditions, as a transport
for them.

## Why

A Midnight contract can emit an event, but the event is public: it records who reacted, when, and to
what. The ledger also limits what an event can be: a 32-byte name, a 256-byte payload, a block-level
byte budget, and about 18 seconds to finality. Parties that need to signal each other privately, at
higher rates and larger sizes than the ledger allows, have no layer for it today. The Midnight node
runs libp2p for consensus but has no publish/subscribe layer for applications.

## Design in brief

- **Sidecar overlay.** Bus Nodes run GossipSub (v1.2: the v1.1 mesh and scoring rules plus
  IDONTWANT) beside the Midnight node, not inside it. Nothing in the node needs to change.
- **Sealed, fixed-size envelopes.** Four body classes (256, 1,024, 4,096 and 16,384 bytes) behind an
  8-byte header and a 512-byte admission slot, so length reveals only a class.
- **Receiver privacy by recognition.** Subscribers receive a whole Shard and recognise their own
  messages locally with salted 16-byte Recognition Tags. The network never learns which messages a
  subscriber wanted.
- **Rate-limited admission.** Each publication carries an admission proof from a registered
  membership, which bounds spam without identifying the publisher.
- **Ledger anchoring.** A Bus Registry contract on Midnight holds memberships, parameters and the
  relay list. Every 60 seconds an Anchor commits to the envelope identifiers seen in that window.
- **Bounded retention.** Store Nodes keep envelopes for 48 hours. A ledger lane carries messages
  through `Misc` contract events when the overlay is not available.

## Status

Midnight Express is at the design stage. There is no proof of concept yet; building one is the next step.
The design document specifies the system and the experimental design that a proof of concept must run.
Exploratory runs guided the design, and the design does not rely on them. The ledger interface was written
in Compact and compiled and costed against the ledger cost model, but nothing has run on a Midnight network.

## Contents

| Path | What it holds |
|---|---|
| [`docs/design-document/Midnight-Express-Design-Document.pdf`](docs/design-document/Midnight-Express-Design-Document.pdf) | The design document: Midnight and the need for private events, the options and requirements, the experimental design, the problem statement, the improvement proposal, the requirements in EARS form (Appendix A) and an annotated reading list (Appendix B). |
| `docs/design-document/draft-final/` | The document source in Markdown; `build/` holds the scripts that assemble it and build the PDF. |
| `design/ears/`, `design/rounds/r5/` | The requirement register. |
| `experiments/` | Exploratory Rust code and the Compact ledger-interface study (`experiments/registry`). Not a proof of concept; see its README. |
| `catalog/`, `notes/`, `graph/` | The research corpus catalog, notes and graph tooling. |
| [`reviews/competitive-event-systems/`](reviews/competitive-event-systems/README.md) | Three independent reviews of each of 26 blockchain, enterprise messaging and listener designs, with extraction decisions. |
| [`catalog/event-systems/`](catalog/event-systems/README.md) | Scrapling primary-source snapshots, retrieval records and hashes for the comparative study. |
| [`docs/product-requirements/`](docs/product-requirements/README.md) | Ten business use cases, feature considerations and candidate EARS extensions for product scope review. |

## License

Apache License 2.0. See [LICENSE](LICENSE).

Recommended implementation direction and ranked product portfolio: [stack and use cases](docs/product-requirements/recommended-stack-and-use-cases.md).

## Architecture showcase

The [interactive architecture page](website/README.md) presents the recommended stack, event journey and ten product priorities. Its [ten-agent study](reviews/architecture-page/README.md) and GPT visual prompts are preserved for review.
