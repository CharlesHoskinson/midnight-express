# privateEvents

Research corpus and design workspace for a **private event bus on the Midnight network**, inspired by
Bitmessage and the decentralized publish/subscribe literature.

The goal is a protocol where events can be published and consumed by agents, smart contracts and
wallets without exposing content, interest or relationships to the infrastructure that carries them.
This repository holds the evidence base, the knowledge graph tooling, and the design work built on it.

## Layout

| Path | Content |
|---|---|
| `catalog/` | One JSON record per paper or spec: title, authors, year, venue, DOI, source URL, status, SHA-256, relevance notes. One file per collection slice, plus the IOG library crawl. |
| `notes/` | Digest per collection slice (queries, gaps, hand-offs) and `midnight-network-stack.md`, a code-grounded read-out of Midnight's node, ledger, indexer and wallet with `path:line` references. |
| `briefs/` | The rules and scope given to the collection agents. |
| `reviews/` | A review of a Bitmessage technical guide. |
| `design/` | Design charter, the twelve designer roles, round runner, Round 1 proposals and Round 2 reviews, plus greppable evidence files (`evidence/`). |
| `graph/` | Extraction, merge, clustering and community-naming scripts for the knowledge graph, and the community labels. |
| `graphify-out/GRAPH_REPORT.md` | Report of the knowledge graph (about 66,000 nodes, 1,100 papers). |
| `scripts/` | Fetch helper (`pe_fetch.py`) with a shared per-host rate limit, open-access upgrade passes, IOG library crawl. |

## What is not in this repository

Paper PDFs and their extracted text are third-party works and are not redistributed. The catalog lists
where each came from, and its SHA-256 lets you check a copy you fetch yourself:

```
~/.local/share/uv/tools/scrapling/bin/python scripts/pe_fetch.py pdf URL SLUG
```

The raw model extractions and the 93 MB `graph.json` are not included either. Rebuild with
`graph/prep.py`, `graph/run_all.py`, `graph/merge.py`, `graph/build.py` and `graph/label.py`.

## Sources

arXiv, OpenAlex, Crossref, HAL, CORE, author and institutional pages, project specifications and
documentation. Paywalled papers have metadata-only records. No paywall or bot wall was bypassed.

## Status

The evidence base and knowledge graph are built. The design exercise is in progress: twelve independent
proposals (Round 1) and cross-reviews (Round 2) are in `design/rounds/`. Requirements in EARS form and a
Rust prototype on rust-libp2p GossipSub are the next steps.
