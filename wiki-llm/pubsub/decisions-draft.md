# Working convergence record

This is the synthesis while the remaining Grok reviews finish. It records design decisions and objections, not a claim of unanimous agent votes. Final reconciliation will appear in consensus.md.

## Evidence already reconciled

The GPT studies establish the current agent-interface inventory, the exact Moth connector contract and actual bounded model validation. The Opus studies independently confirm the private local watch/journal boundary and identify additional deployment and interoperability constraints. Initial topic-routing language in the wallet study was rejected and corrected before integration. Initial provider runs that hit tool-turn limits are recorded as incomplete; their assigned researchers continue using collected evidence.

## Adopted direction

| Question | Working decision | Reason |
|---|---|---|
| Does pub/sub require a third network protocol? | No new mandatory broker or network pub/sub protocol selected. | Whole-shard transport and local recognition already define the private boundary. Recovery and control-plane integration still need custom software. |
| Where do subscriptions live? | A principal-bound private watch service with a single-writer consumer journal. | Durable cursor ownership cannot be supplied by wallet sessions or lossy notification connections. |
| What does a slow consumer change? | Only local scheduling and credit. | Match-dependent network intake or repair would reveal interests. Whole-shard resource policy remains independent. |
| What can an agent do? | Read bounded typed data using a revocable human-provisioned grant; prepare actions only under separate scope. | Sender text, notification arrival and UI approval cannot supply consequential authority. |
| Which event formats work now? | Exact quote, invoice-observation and sandbox-approval profiles. | Actual fixture checks accept at supplied historical context and retain executes:false. Other categories remain mocks. |
| How is Moth connected? | Explicit, exact-version connection/status adapter, without polling or signing. | The verified implementation supplies no narrow grant or DApp revoke method. |
| Is Pages a suitable wallet origin? | Demo connection requires acknowledgement; recommend a dedicated origin for production. | Other project pages share the owner origin and its Moth grant. |
| What does the dashboard prove? | Local interaction and bounded state transitions over synthetic data. | It has no transport, decryption, live permission, browser validator, durable database or business effect. |

## Objections preserved

A browser inbox may confuse coverage with matching activity. The human-experience study recommends received/checked/reviewed progress and user testing. Raw cursors remain useful in this engineering demonstration; production terminology and source preferences need testing.

The agent study prefers MCP Apps for in-host supervision and a Python SDK adapter based on observed current support. The architecture retains a Rust core and TypeScript-facing application SDK; adapter implementation language and host compatibility remain gates. None of these choices adds an admission dependency.

Opus privacy prefers a dedicated wallet origin or explicit acknowledgement on Pages. The demo chooses acknowledgement and clear origin scope; this does not reduce the grant itself. Production should use a dedicated origin.

Actual sealed payload sizing, recognition CPU cost, RLN class-credit compatibility, Store repair and mobile whole-shard feasibility remain unresolved original protocol obligations. JSON byte estimates or a functioning interface cannot close them.
