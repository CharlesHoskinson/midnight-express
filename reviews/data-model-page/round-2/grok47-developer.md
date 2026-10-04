<!-- Review via Grok CLI; selected model: grok-4.7; baseline: f0e3fc6. Recommendations require editorial/factual review. -->

# Data model page: developer-experience review

The page states the design and the measured bounds. These seven passages add the procedure a reader needs: which profile to install, how the bundle is pinned, what an adapter emits, which identity governs a retry, and what a chain fixture proves.

### 1. Choose the profile by its type string

Paste after the lead in `#problem`, before the three cards.

> Start by naming the decision a message is allowed to support, then choose the one closed profile that can express it. `rfq.v0.2` with type `mpe.rfq.quote.v0.2` is a whole-share USD quote. `invoice.v0.2` with type `mpe.invoice.payment-observed.v0.2` is an observation of a payment against one invoice. `agent.v0.2` with type `mpe.agent.approval.v0.2` is one sandbox WriteReport proposal. Fill every required term of that profile. Fractional shares, a second currency, a fee schedule, invoice allocation, or another agent tool each call for a separate reviewed contract. The shared fields identify source, occurrence, time, type, and contract. The business terms stay in the profile you selected.

### 2. Map the displayed quote through the declared adapters

Paste in `#example` after the agreed-meaning block, before the section note.

> Use the two shipped adapters as the pattern. The TypeScript adapter takes dollars per share, $123.45, for a buyer purchasing 100 shares. The Rust adapter takes cents per 100 shares, 1,234,500 cents, for the dealer selling those shares. Both, on the attested fixture, produce coefficient 12345, scale 2, quantity 100 whole shares, cash 1,234,500 cents, a declared requester perspective, and fees set to None. Fifteen adapter cases cover this pair. Missing price basis, a contradictory cash total, an unsupported fee, or an unknown field refuses. The intent digest is SHA-256 over JCS of domain `mpe.model.intent.v0.2` together with source, type, profile, contract, and data. Leave occurrence id, event time, and the outer EID out of that object. A second dealer with the same economics receives a different digest because source is inside it. Keep the source bytes with the mapping.

### 3. Pin the bundle and separate meaning from code

Paste in `#contracts` after the three layer cards, before “An exact agreement”.

> Install a profile by the hash of its bundle. `bundles/<manifest-sha256>/` contains `manifest.json`, `schema.json`, `core.json`, and `rules.json`. The contract commitment is the fingerprint of the JCS manifest. `profiles/installed.json` allowlists exact commitments, and `profiles/lock.json` holds the current aliases. A message passes when `mpeprofile`, `type`, and `mpecontract` match that installed snapshot. An unknown commitment refuses. v0.1 remains a historical read-only release. Dispatch uses the v0.2 loader. A new price basis, clock rule, or approval scope is a new bundle and a new commitment. A fix that preserves the rules keeps the commitment and is recorded as implementation evidence. `negotiate` returns the intersection of the commitments both sides have already installed. Python, Rust, and TypeScript agree on the RFQ campaign. Invoice and approval semantics are checked by the Python reference, and the sandbox host is covered by the PostgreSQL checks.

### 4. Give the cleartext shape before the first encode

Paste directly after the previous paragraph, still in `#contracts`.

> Put these ten fields in the proposed encrypted body: `specversion`, `id`, `source`, `type`, `time`, `datacontenttype`, `dataschema`, `mpeprofile`, `mpecontract`, and `data`. Compare each id as exact bounded ASCII. Write `time` as Gregorian UTC at second precision, `YYYY-MM-DDTHH:mm:ss.000Z`, years 0001 through 9999. Offsets and leap seconds fall outside that form. Express money and quantities as bounded decimal strings, USD at scale 2 and whole shares and Step at scale 0. Keep integer tokens nonnegative and at most 9007199254740991. The parser accepts up to 3926 raw UTF-8 bytes, depth 12, 512-character strings, and arrays of 16 items. Floats, exponents, and duplicate keys fail. Whitespace is significant. Leave room beyond that cleartext for sealing.

### 5. Make the three identities decide the retry

Paste after the lead in `#replay`, before the two columns.

> Ask three questions on every retry. The event id asks whether this occurrence is already stored: identical content is a duplicate, and changed content conflicts. The intent digest asks whether the business content matches; a new event id leaves that digest's inputs unchanged. The action key `(authorityDomain, executionScope, actionId)` asks whether the work has been consumed. For `agent.v0.2` the work is one WriteReport. Changing the target or the contract is a conflict, so the consumed action stays consumed. The host records inbox, dedup, the report row, the Step charge, outbox, checkpoint, and cursor in one PostgreSQL transaction. It reserves the approved Step maximum, charges one write, and releases the unused remainder. Inside the 56 PostgreSQL checks, the run killed four worker processes: after the effect writes, before commit, after commit and before acknowledgement, and after a separate destination-fixture commit. Recovery retained one report-row effect. A lost destination reply stays `OutcomeUnknown` until the original idempotency key is reconciled.

### 6. Tell the reader what a chain projection is allowed to prove

Paste after the lead in `#chains`, before the Ethereum and Solana columns.

> Of the 291 vocabulary entries, two have read-only fixture projections: an ERC-20 Transfer from a supplied receipt and logs, and a legacy Token Program TransferChecked. A projection keeps the raw amount, zero and the maximum included, with physical inclusion or instruction identity and decoder identity. An ERC-721-shaped log refuses. Token-2022 sits outside the Solana slice. The 28 fixture checks include exact amounts, failed execution, repeated inner calls, rollback, re-inclusion, and replay. Re-inclusion is stored at a new physical location, and the earlier observation stays in the journal. Conflicting finality assertions are recorded as a gap. `sourceDigest` identifies the fixture's deterministic JSON, and the Solana branch hash arrives as its own supplied field. Treat the slice as a decoder check on those fixture bytes. Chain amounts keep uint256 and u64 primitives of their own.

### 7. Turn getting started into a first successful run

Paste after the numbered list in `#start`, before the FAQ.

> Work through the reference commands in `model/README.md` before writing a new adapter. Sync `model/requirements.lock.txt` with hashes into an isolated environment, build the locked Rust crate, and run `model/test_conformance.py`, `model/test_bundles.py`, `model/test_catalog.py`, `model/test_interoperability.py`, and `model/test_chain_observations.py`. Typecheck `model/interpreters` on Node 24 or newer. That compiler pin is separate from the semantic commitment. Run `model/recovery/test-postgres.mjs` on isolated PostgreSQL 17.11 and Umbra commit `f662822765247f0da553347c9819f958a1992d28`, the tree whose package metadata is 0.9.5. Those commands exercise the published corpus: 35 RFQ vectors (4 accepted, 31 safe refusals) across Python, Rust, and TypeScript, 28 chain fixture checks, and 56 PostgreSQL checks with four worker kills and one report-row effect. For a partner conversation, bring the commitment both sides will install, the adapter receipt for their convention, and the name of the owner for source authentication and destination reconciliation. Integration hours and customer ROI are still uncollected. Measure the pilot and file the result beside these counts.

If this revision can take only three passages, use the profile strings, the bundle pin, and the three retry questions.
