# Subscription research

The research asks how humans and agents manage subscriptions, how wallets and DApps connect as consumers, and whether the current data contracts support useful application behavior. It also asks whether the existing stack is sufficient or needs additional components.

[Agent reports](agents/) preserve approaches, intermediate results, objections and recommendations. [Sources](sources/) holds Scrapling text/raw captures and PixelRAG screenshot tiles with retrieval metadata. [Consensus design](consensus.md), [progress notes](progress.md) and [provider provenance](surge.json) reconcile the reports. The [local contract](../../design/subscriptions/README.md), [requirements](../../docs/product-requirements/pubsub-subscription-experience.md) and [dashboard](../../website/dist/subscriptions.html) apply the findings.

The original wire protocol and requirement register remain authoritative. Local subscription selectors must not become business topics or upstream filters. Wallet connection, publication admission, source authentication and permission to act remain separate decisions. The demonstration uses mock event delivery; wallet connectivity has its own explicit consent flow.
