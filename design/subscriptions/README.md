# Proposed local SubscriptionIntent contract

This closed JSON Schema describes local subscription configuration for the research demo. It is not an MPE wire extension, production SDK, installed model profile or permission grant. The selector operates locally after authorized whole-shard intake/decryption. Preserve original sealed wire separately from derived events and views. Do not expose category/profile/source selectors as relay topics, routes or processing acknowledgements.

See [the researched contract](../../wiki-llm/pubsub/subscription-contracts.md), [offline model-fit evidence](../../wiki-llm/pubsub/data-model-fit.json), [dashboard](../../website/dist/subscriptions.html) and [current model boundaries](../../model/README.md).

`local-subscription-intent.schema.json` closes every object and requires every field. It fixes the three existing v0.2 profile commitments; contracts, credentials and ops use `mock.local.v1`/`mock-only` and never enter model dispatch. Local handle prefixes distinguish subscription, principal, shard, sink and cursor. Arbitrary URL sinks, sender expressions, unknown fields, category/profile mismatches and unsafe configured limits refuse. `sourceEquals:[]` selects all sources already authenticated and authorized by local business validation policy. Anonymous transport membership alone authenticates no business source. Permitted predicates are all, payment-final (invoice only) and approval-report (agent only).

Dashboard export uses this shape with latest/empty cursor initially, or explicit after/cursor following gap acceptance, bounded local sink and opaque owner/shard handles. The dashboard persists bounded synthetic runtime history and intent revisions in IndexedDB. Its numeric positions remain simulation metadata, not authenticated journal-issued cursor capabilities. Reload never restores current delivery authority. See the [workspace audit](../../reviews/subscription-workspace/README.md). Requested state is active/paused/unsubscribed. Expired/revoked/gapped are runtime outcomes and cannot be requested to override a permission decision.

Intent revision history must be immutable: the same `(subscriptionId,revision)` may only repeat identical canonical content. A change creates a strictly greater revision through local compare-and-swap. Runtime state is separate: current state, delivery/processing checkpoints, oldest retained cursor, explicit gap and bounded counters. Pause preserves checkpoints; resume rechecks permission, expiration and retention; unsubscribe preserves a tombstone and action ledger. Revision monotonicity and these transitions require runtime implementation and are not schema assertions.

For after, the cursor is exclusive and must resolve to the same journal/shard. Earliest/latest require an empty cursor and resolve atomically at installation. A retention gap cannot silently jump to latest. Explicit gap acceptance creates a new revision. Processing receipts remain private; delivery receipt does not establish successful effects. Replay retains original occurrence identity and stable approval action identity and rechecks current permission.

Run the finite schema checks with the existing model validation environment:

```sh
/tmp/mpe-data-model-validation-env/bin/python design/subscriptions/test_contract.py
```

The script checks six compatible category profiles, predicate compatibility, cursor modes, allowed intent states, limits, required fields, nested closure and rejected remote/executable routing fields. It installs an explicit Gregorian date-time format checker because JSON Schema format can otherwise be annotation-only, and Python environments may lack an optional RFC3339 checker. Production validators must enable equivalent format assertions and enforce the strict timestamp pattern. JSON Schema integer validation cannot inspect lexical JSON tokens; the intake parser must additionally refuse floats/exponents, duplicates, invalid UTF-8, excessive bytes/depth and unsafe integers using the model discipline.

## Integration and acceptance gates

- Authenticate the local principal and verify current shard/configuration/sink permission. A structurally valid local handle must resolve through trusted local allowlists; it is not proof of permission. Check exclusive expiration against trusted local time and recheck revocation before callbacks/effect preparation.
- Install exact authenticated model bundles through an allowlist; source admission and complete evidence remain separate. Do not fetch sender `$ref`, dataschema or sink URLs. New model releases require explicit schema revision/review, with no implicit fallback.
- Implement durable intent CAS, journal-bound cursor ownership, atomic high-water snapshots, bounded event/byte credits, retention-gap visibility and durable quarantine disposition. Test crashes and races across intake, processing and checkpoint advancement. The demo supplies none of these persistence guarantees.
- Retain original wire where genuine sealed bytes exist, keep mock JSON distinct, and separate occurrence/action conflicts. Exercise replay, revoked/expired approval, unknown commitments and sink saturation without re-executing consumed actions.
- Test that selectors, match status, human processing decisions and private receipts never leak to relay metadata. Whole-shard membership still exposes the whole shard to an authorized reader; this contract does not provide finer cryptographic segmentation or conceal traffic timing.
- Label offline fixtures with exact event/context JCS hashes and October 4 noon trusted clock. Every accepted v0.2 reference result has `executes:false`; no browser schema check substitutes for current production authority or authenticated original wire.

Finite checks validate configuration boundaries. Schema validation does not implement execution authority, durable consumers, transport privacy or global exactly-once effects.


## Directory workspace recommendation

The [subscription workspace design](directory-workspace.md) defines the researched replacement interface: directory-first discovery, independently scoped feeds, personal organization, historical information restoration and separate delivery attention. It is a recommendation, not the current dashboard implementation. Feed descriptors map to existing local intent bindings through an adapter; they add no fields to the closed intent or sealed business envelope. The [council archive](../../wiki-llm/subscription-design-council/README.md) records evidence and resolved disagreements.
