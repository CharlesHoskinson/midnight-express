# Midnight Express

Midnight Express is a proposed delivery system for confidential messages between applications, organizations, wallets and software agents on [Midnight](https://midnight.network). It combines a private messaging overlay with rules for interpreting business updates and recovering unfinished work.

Consider a buyer asking several dealers for a quote. Each dealer may use a different price convention. The buyer needs to receive the replies privately, compare their meaning and reject expired offers. If its application disconnects, it needs to resume without treating a repeated reply as a new instruction. Midnight Express brings these responsibilities into one design, while the participating applications retain control over business decisions.

The intended value is less custom integration and manual reconciliation across organizations. The first proposed pilots cover quote coordination, invoice payment observations and human-approved software actions. Partner integration costs, turnaround improvements and customer savings still need to be measured.

## How it fits together

The delivery overlay uses [GossipSub](https://github.com/libp2p/specs/tree/master/pubsub/gossipsub) beside the Midnight node. Publishers seal messages into envelopes. Receivers take a whole shard of traffic and recognize their messages locally, so delivery operators do not need business subscription filters. Encryption protects content; connections, timing, shard participation and envelope size classes can remain visible. The design makes no general claim of relationship privacy against a global observer.

Membership and rate-limited admission control publication. The recommended membership module adopts Semaphore's identity and witness lifecycle patterns within one compatible RLN-style admission proof. Midnight's proposed Bus Registry provides the authoritative membership state. Ledger anchors commit to batches of envelope identifiers. A publication proof or anchor does not authorize a trade, payment or other business action.

Applications agree on a small shared data core and a precise contract for each workflow. An adapter translates a participant's declared format into that contract and refuses missing or contradictory meaning. The current reference covers a quote, a payment observation and an approval. Each keeps its own terms and authority rules.

Recovery records the accepted message, logical action, local effect and processing progress together. The recommended backend uses UmbraDB with PostgreSQL; standalone clients use SQLite. Remote effects also need the destination's idempotency and reconciliation rules. The local sandbox demonstrates one database report-row operation, with fixture authority, rather than financial execution.

## What exists today

The full Midnight Express protocol remains a design. Its [design document](docs/design-document/Midnight-Express-Design-Document.pdf) defines the wire format, privacy requirements, operating assumptions and proposed experiments. Exploratory transport code and a compiled Compact ledger-interface study are available under `experiments/`; they do not establish a deployed protocol or completed proof of concept.

The [v0.2 reference implementation](model/README.md) checks bounded business contracts and compares RFQ interpretations across Python, Rust and TypeScript. It also projects supplied Ethereum and Solana transfer fixtures and exercises Umbra/PostgreSQL recovery through worker crashes. These checks cover local behavior under declared fixture assumptions. Genuine admission proofs, finalized Registry integration, live source authentication, replicated retention and production operations remain work for the [prototype plan](docs/product-requirements/prototype-sprints.md).

## Read and explore

The [website](https://charleshoskinson.github.io/midnight-express/) explains the product, its workflows and recommended stack. Its [Data Model guide](https://charleshoskinson.github.io/midnight-express/data-model.html) shows how participants agree on meaning, and its [Implementation page](https://charleshoskinson.github.io/midnight-express/implementation.html) describes the proposed validation stages.

Repository material is organized by purpose:

| Material | Where to start |
|---|---|
| Product direction and candidate use cases | [Recommended stack and use cases](docs/product-requirements/recommended-stack-and-use-cases.md) |
| Business meaning and integration rules | [Unified data model](docs/product-requirements/unified-data-model.md) |
| Reference behavior, reproduction and deployment gates | [Model guide](model/README.md) and [implementation assessment](docs/product-requirements/data-format-implementation.md) |
| Ethereum and Solana application domains | [Ethereum](docs/product-requirements/ethereum-application-domain.md), [Solana](docs/product-requirements/solana-application-domain.md) and [proposed vocabulary](model/domains/README.md) |
| Protocol specification and document sources | [Design document](docs/design-document/Midnight-Express-Design-Document.pdf), `docs/design-document/draft-final/` and `design/ears/` |
| Literature and comparisons | `catalog/`, `notes/` and [comparative design assessments](reviews/competitive-event-systems/README.md) |
| Local website maintenance and publishing | [Website guide](website/README.md) |

## Private subscriptions

The [subscription design](docs/product-requirements/pubsub-subscription-experience.md) explains how humans, wallets, DApps and agents follow supported workflows. Try the [dashboard](https://charleshoskinson.github.io/midnight-express/subscriptions.html), or inspect the [research record](wiki-llm/pubsub/README.md). The dashboard uses mock delivery, offline-checked reference fixtures and optional explicit Moth connection controls.

## Formal data model

The [Lean specification](formal/lean/README.md) makes the installed v0.2 semantic rules precise. Read the [Specification guide](https://charleshoskinson.github.io/midnight-express/specification.html) for quote arithmetic, payment evidence, scoped approvals and the proof assumptions.

## License

Original project code and documentation are released under Apache License 2.0; see [LICENSE](LICENSE). Imported reference materials and fonts retain their own licenses and attribution; see [NOTICE](NOTICE).
