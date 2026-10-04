# Data-format recommendations: v0.2 implementation status

v0.2 corrects the parsing and replay defects identified in [the original review](data-format-review.md). It adds independent RFQ interpretation, offline contract bundles, read-only chain projections and a recovery sandbox. These are local implementations with synthetic trust assumptions. Completing the three protocol sprints and establishing production readiness still require the deployment evidence described below.

| Recommendation | Implemented artifact | Measured evidence / remaining boundary |
| --- | --- | --- |
| DFR-01 exact parsing | v0.2 parser, portable strict schemas, independent Rust/TypeScript parsers | Original LF/rounding counterexamples reject, and coefficients remain exact strings. Recorded coverage: 80 Python checks and 35 cross-language RFQ vectors. |
| DFR-02 occurrence/action identity | Python occurrence recording and public-API Umbra host | Duplicate-action occurrences now record immutable identity; exact repeat becomes duplicate-event, changed repeat conflicts. Scope/retarget and concurrent replay tests pass. |
| DFR-03 invoice semantics | All-status amount bound and record-creation clock definition | Pending/Final/Reversed below/equal/above-payable matrix; `effectiveAt <= observedAt <= event.time <= trustedNow`. No bank-finality or accounting authority inferred. |
| DFR-04 catalog correction | 291-entry versioned vocabulary, semantic index, lifecycle support matrix | Instruction versus RPC, submission responses, nonce/rewards and Token-2022 configuration clarified; 14 checks cover catalog metadata. Changed classifications have new IDs with supersedes; original catalog preserved. No generic RPC dispatcher. |
| DFR-05 independent agreement | Separate Rust/TypeScript interpreters and format-owned RFQ adapters | Canonical event/intent bytes and digests agree with Python, with zero accepted disagreements in the finite corpus of 35 vectors, 15 adapter cases and three ordered replay cases. Fixtures are unsigned. |
| DFR-06 immutable contracts | Content-addressed standalone bundles, verified read snapshot, exact intersection helper, separate release/dependency evidence | Integrity, no remote/dynamic refs, path/symlink checks, coexistence and independent profile changes are covered by nine bundle tests. Exact original v0.1 preserved read-only; current loader cannot dispatch it. Authenticated installation/live migration remain gated. |
| DFR-07 lineage/temporal data | Read-only SQLite source-fact/delivery/invalidation journal | Physical facts dedup independently of observer deliveries; branch re-inclusion, repeated CPI, known-at views, conflicting native assertions and gaps tested. No complete-history or consensus proof claim. |
| DFR-08 chain slices | ERC-20 receipt/log projection and legacy SPL TransferChecked projection with closed schema and exact raw quantities | The 28 fixture checks cover zero/max uint256/u64, failed transaction/CPI, repeated CPI, missing evidence, rollback/re-inclusion and restart. Unknown CPI success refuses; Token-2022/new transaction versions are outside the base slice. Live authenticated RPC and independent full program decoders remain promotion gates. |
| DFR-09 effect boundary | Fixture-authorized one-operation Umbra/PostgreSQL sandbox host | A report-row write commits atomically with budget, inbox/action/outbox/checkpoint/cursor state. Recorded coverage: 56 checks and four actual worker kills on PostgreSQL 17.11 and Umbra commit `f662822765247f0da553347c9819f958a1992d28`. Uncertain destination acknowledgement reconciles its original key. Production capabilities/financial execution remain outside scope. |
| DFR-10 measurements | Executed golden vectors/results, adapter receipts, local projection/recovery reports, measurement template | Actual finite-corpus counts are saved; real partner integration hours, source quality and ROI remain explicitly uncollected rather than reported as zero. |

## Reproduce

[model/README.md](../../model/README.md) contains pinned dependency/build/test commands and the PostgreSQL integration command. [model/evidence](../../model/evidence/) contains machine-readable results, raw conformance vectors, mapping receipts and separate implementation release evidence. The original review's counterexamples still reproduce through the archived v0.1 interpreter; `--current` checks their corrected v0.2 outcomes.

The independent campaign contains four accepted RFQ cases and 31 refusals. That finite synthetic sample does not estimate a live-data error rate. Adapter equivalence uses identical complete attested intent in two source encodings. Distinct dealer identities must keep distinct intent digests even when price economics agree. No signature on source bytes is reused over transformed bytes.

## Authority and scope

The sandbox gets its permission context from a deliberately trusted test fixture. Its only operation, WriteReport, writes one database report row. One Step is the budget unit for that atomic write: the host reserves the approved maximum, charges one and releases unused capacity.

The approved intent binds the authority domain, execution scope, policy/budget window and stable action ID. Tenant scope must remain part of that commitment; a caller cannot replace it per call. The host rechecks permission inside the effect transaction. Reading history or reconciling an outcome grants no new permission to act.

The outbox destination is a separately committed acknowledgement fixture. The tests kill the worker after that destination commit and preserve Dispatching/OutcomeUnknown until reconciliation. They do not exercise a bank, blockchain transaction or arbitrary agent tool. External exactly-once behavior still requires the actual destination's verified idempotency/reconciliation contract.

## History and installation

Original v0.1 code/schema/fixtures and known defects remain unchanged in a historical release. Active semantic commitments are separated from implementation source hashes; an invoice implementation edit no longer changes RFQ or approval meanings automatically. Old/current semantic bundles can be installed together by exact commitment, but unsafe v0.1 is read-only. Deployment still needs an authenticated installer, downgrade policy and a procedure for migrating active workflows. A local SHA-256 comparison verifies content only.

## Chain evidence and remaining promotion gates

Read-only chain projections consume bounded supplied RPC dictionaries and trusted fixture context. Source digests identify deterministic fixture serialization; branch/decoder/context identity and exact raw units are explicit. Solana CPI success requires instruction-level evidence: overall transaction success is insufficient when an inner failure is caught. Finality remains a native source assertion. The journal never establishes dataset completeness on its own, and conflicting assertions produce a gap.

Live support requires evidence tied to the deployed program, ABI and code, authenticated provider data, and independently verified decoder/finality policy. Each admitted workflow also needs complete typed payloads and a policy for authorized evidence retrieval and retention that preserves privacy. The 291-entry vocabulary remains proposed. Protocol integration additionally retains genuine admission/wire/security/replicated-availability gates; none is substituted by local conformance tests.
