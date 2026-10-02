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

Midnight Express is at the design stage. The requirements have been derived and reconciled, a Rust
prototype on rust-libp2p has been built and exercised in simulation, and the ledger interface has been
compiled in Compact and costed against the ledger cost model. It has not run on a Midnight network, and
the prototype's admission proof is a stand-in, so none of its figures should be read as production
measurements.

The design document, the Midnight Improvement Proposal and the accompanying Problem Statement will be
published here.

## Related work

The research corpus and design workspace behind this project are in
[privateEvents](https://github.com/CharlesHoskinson/privateEvents).

## License

Apache License 2.0. See [LICENSE](LICENSE).
