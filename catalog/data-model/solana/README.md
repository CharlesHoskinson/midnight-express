# Solana primary-source archive

Collected 2026-10-03 with Scrapling `Fetcher.get`, TLS verification enabled. This archive supports [the proposed Solana application domain](../../../docs/product-requirements/solana-application-domain.md); it does not implement an SDK or validate finality.

`manifest.json` and per-source metadata record original/resolved URL, UTC retrieval time, HTTP status, raw and extracted-text paths/digests, and HTTP-level evidence usability. `raw` files preserve fetched response bodies; extracted text is a reading aid. SHA-256 establishes local integrity, not publisher authentication. Documentation and moving GitHub branches are snapshots, not pinned deployed program/code versions. The source URLs are authoritative links for attribution; review redistribution/license terms before publishing full third-party content.

The initial `wormhole-solana` shim URL returned 404 and is retained only as a failed-fetch record. `wormhole-core-solana` supplies the successful replacement. `getstakeactivation` returns HTTP 200 after redirect to a removed-method page: this is evidence of removal in Agave v2.0, not evidence that the RPC method is supported. Unstable block/slot-update/vote subscriptions require explicit provider capability and schema-version pinning; a documentation fetch cannot prove provider availability. `evidence_usable` records HTTP success only and must be interpreted with these semantic caveats.

Reproduce with the project's research environment:

```bash
/tmp/midnight-scrapling-env/bin/python catalog/data-model/solana/fetch_sources.py
```

Refetching updates the snapshots and digests. Runtime validation must use locally reviewed contracts and adapters; never fetch this documentation or a sender-provided IDL/schema during effect handling. The archive deliberately preserves conflicting shorthand about blockhash age; applications should use explicit last-valid-block-height and pinned runtime rules instead of copying a wall-clock/slot timer.
