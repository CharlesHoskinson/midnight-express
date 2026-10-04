# Financial semantics evidence archive

Collected 2026-10-03 after online primary-source discovery. See [research review](../../../reviews/data-model/financial-semantics.md) and [manifest](manifest.json).

`manifest.json` lists 24 fetch records with requested URL, UTC collection time, Scrapling method, HTTP status or error, extracted-text filename, byte size and SHA-256. Nineteen records contain substantive successfully extracted text; that count includes supplemental redirect renderings and API metadata, not nineteen independently assessed standards. HTTP errors, empty output and namespace-only content remain in the manifest for auditability.

Core primary evidence: FINOS product/pretrade/namespace documentation, repository README and license, pinned FINOS math/observable/settlement model sources, ISDA FpML standards/expiry/historical introduction, FIX Trading Community SBE source, ISO 20022 business model/data dictionary, and OASIS UBL Invoice model. Historical FpML 4.4 and release-candidate SBE are labeled accordingly in the review. FIXimate redirected to Orchimate; these snapshots are supplemental and do not establish primary standard text or side conventions.

The `.txt` files are `get_all_text()` extraction, not raw HTTP payloads. Whitespace/markup are normalized by extraction, including markup interpretation within code/JSON; do not parse API metadata snapshots as original JSON. Hashes verify these stored text artifacts only. `collect.py` and `collect-extra.py` preserve the initial collection calls; three pinned model files were additionally collected using the same Fetcher call. Re-running scripts against mutable URLs can change archived evidence, so copy the archive before refresh.
