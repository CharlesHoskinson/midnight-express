# Style sheet for the design document

The document is written by an unnamed author for engineers, researchers and decision-makers. It speaks in its own voice, in the
present tense, and describes, judges and recommends. A reader must believe that a person wrote it in one sitting from public sources,
the Midnight code and the project's own measurements.

## It must not know how it was made
Never write, in any form: agent, model, LLM, GPT, Claude, Opus, Sonnet, Sol, Grok, Luna, Codex, prompt, round, designer, reviewer,
judge, builder, panel, persona, seat, council, scoring, "desk", draft, revision, earlier version, "we asked", "the team asked",
"fetched", "scraped", "the source files", "automated". Do not narrate research ("a search found", "could not be read"), do not mark claims
"unverified", do not mention the file names or folders of the working material (`design/`, `notes/`, `catalog/`, `LEARNINGS`, `RECONCILE`
and the like). Do not describe the document's own structure at length ("this chapter will"). State the content.

Substitutions that are allowed:
- The prototype work is "three independent implementations of the same specification" and "the reference implementation" (the one selected). Name
  them Implementation A, B and C only when a difference between them matters.
- The requirement set and its decisions are "the requirement set" and "the decision register" (identifiers MPE-FMT-001, DEC-003).
- Expected results before an experiment are "hypotheses" and "expected results"; they have pass conditions. Never write "predicted".
- Results are "measured", "derived" (arithmetic from stated inputs) or "assumed". Use those words naturally; do not tag with brackets.

## The name
The system and the proposal are called **Midnight Express**. Chapter 1 introduces it once ("Midnight Express is the proposed private event system for Midnight"). After that, write
"Midnight Express" when you mean the system, in every chapter, and "the system" or "the design" only when the sentence is clearly about it. Do not use "MPE", "the bus" or "the
private event bus" as a name; "private event bus" may still be used as a plain descriptive phrase. Requirement identifiers keep their prefix (`MPE-FMT-001`, for Midnight Private
Events, the subject of the requirements). Do not explain how or when the name was chosen.

## Voice and prose
- Plain, specific, concrete. Prefer a number, a name or a mechanism to an adjective. Show the arithmetic for any derived figure.
- No em dashes. Use commas, colons, parentheses or full stops.
- Banned filler: delve, leverage, robust (say "resilient" or state the property), seamless, crucial, pivotal, landscape, tapestry, realm,
  underscore, showcase, "it is important to note", "not just X but Y", "in order to", "in today's", "game-changer", "cutting-edge".
- No rule-of-three padding, no inflated claims, no promotional tone, no rhetorical questions, no summary sentence that repeats the paragraph.
- Vary sentence length. Short sentences for claims, longer for reasoning. Active voice. First person plural is not used; "this document".
- Every paragraph earns its place. Do not repeat across chapters; refer to the chapter or requirement that owns the point.
- Do not claim stronger privacy than the document defines. State limits where they bind.
- Explain a term at first use, then use it consistently. Use the glossary terms exactly: Event, Envelope, Shard, Tag, Bus Node, Store Node,
  Publisher, Subscriber, Consumer, Admission Proof, Registry, Anchor, Ledger Adapter, Indexer, Operator.

## Citations and facts
- Cite literature with pandoc keys: `[@2012-voulgaris-poldercast]`, several as `[@key1; @key2]`, with locator `[@key, p. 12]`. Use only keys listed in
  `build/bibkeys.txt` (the works that were read). The catalog slug is the key. Do not invent a key, an author or a number.
- Cite Midnight and libp2p code in a footnote: `^[midnightntwrk/midnight-ledger, onchain-vm/src/vm.rs, constant MAX_LOG_EMITTED; main branch, accessed 1 October 2026.]`.
  Name the public repository, the file path and the symbol; never a local path.
- Requirement identifiers are written `MPE-FMT-001` in monospace; decision identifiers `DEC-003`. Parameters `P-FMT-1`.
- Statements about Midnight must say which code generation they come from when the published documentation and the code differ.
- Numbers carry units. Use KiB for 1,024 bytes where the source does, and write "1,000,000 B" or "1 MB" consistently with the source.

## Layout rules (Markdown for pandoc)
- `#` starts a chapter: `# Midnight in brief {#ch2}`; `##` sections; `###` subsections. Do not number headings by hand; the build numbers chapters.
- Tables: pipe tables with a header row. A short sentence before the table says what it shows.
- Diagrams are provided as figures (see FIGURES.md). Do not draw diagrams in text; do not use ASCII art. Code and byte layouts may use fenced blocks.
- No HTML, no emoji. Footnotes with `^[...]`. Lists only for parallel items, never to break up an argument.

## Honest scope
The privacy claims are the limited ones in the requirement set: content confidentiality and interest-hiding from infrastructure, no claim
against a global observer, no timing or relationship privacy at launch. The admission mechanism in the prototype is a stand-in whose secrets
the relays can see. Say so wherever it matters.

## Vocabulary (binding; the Foundation's meanings come first)
"Event" and "private event" are the Foundation's terms: an event is a contract event emitted by a Compact circuit and recorded in a transaction (MIP-0002); a **private event** is a contract event some of whose fields are encrypted for chosen recipients and bound to the transaction by a commitment the proof checks (MPS-0005, Part 2, planned). Midnight Express does not redefine either. Our terms:
- **Message**: the application message a Publisher seals and delivers (not a contract event). **Confidential Message**: a Message that holds the four properties of Chapter 4. **Carried event**: a Message whose payload is the unchanged bytes of a contract event, public or private, with the transaction hash and position.
- **MPE Envelope** (never call `VersionedLogItem` an envelope); **Shard** (never "topic" except "GossipSub topic"); **stream** (not "logical topic"); **Recognition Tag** (not "Tag"); **Bus Node**, **Store Node** (never just "node"); **Bus Registry** (not "Registry"); **Bus Operator** (not "Operator"); **ledger lane** (not "fallback"); **admission window** (not "epoch"); **admission nullifier** and **consumption nullifier** (never bare "nullifier"); rollout **Stage 0, 1, 2** (never "Phase", which belongs to MPS-0005); **Anchor** stays; **Ledger Adapter** stays (never "bridge"); **Indexer** uses the Foundation's definition: a service that reads chain data and serves it to wallets and DApps.
- Midnight Express is a complement to on-chain private events and, under stated conditions, a transport for them. It is not an alternative to them. It does not replace MPS-0005 Part 2.
- Titles: the document keeps "Midnight Express: Private Events for Midnight"; the MIP is "Midnight Express: Confidential Message and Private Event Delivery over a GossipSub Overlay with Ledger Anchoring"; the MPS is "Confidential Message and Private Event Delivery for Contracts, Agents and Wallets" (MPS-xxxx).
- The text carries no trace of revision: never write "formerly", "renamed", "earlier draft", "alignment study", "audit" or similar. Cite the Foundation's documents and the GossipSub specifications as ordinary sources.
