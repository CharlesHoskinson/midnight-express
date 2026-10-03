# Design document outline

Title: **Midnight Express: Private Events for Midnight**
Subtitle: Requirements, Options and an Experimental Design on GossipSub

Audience: engineers and protocol designers who build on or operate Midnight, privacy and distributed-systems researchers who review
the design, and decision-makers who choose what to fund. The document must stand alone: a reader who has never seen the underlying work
can follow it and check its claims against public sources.

## Front matter
- Title page, contents.
- **Executive summary** (900 words): the problem, the definition of private events, the options, the recommended design, what a first
  implementation showed, and what is still unknown. Written last.

## Part I. Midnight and the case for private events

**1. Introduction** (1,200 words). Purpose and scope; what the document decides and what it leaves open; conventions (requirement
identifiers, the EARS syntax, how claims are marked as measured, derived or assumed).

**2. Midnight in brief** (3,500). What Midnight is and how it works, at the level a protocol designer needs: the partner-chain
architecture and consensus; the node and its peer-to-peer layer; the ledger (shielded and unshielded state, DUST and NIGHT, fees);
Compact contracts and zero-knowledge proofs; the indexer, wallet and dapp connector; what the chain already offers for events (the
`emit` mechanism, its 32-byte name and 256-byte payload, the 1 KiB limit, public visibility, finality) and what it does not (no
publish/subscribe layer, no gossip protocol beyond consensus, no private event primitive). Include a table of the limits that bind any
event design and say which generation of the code each fact comes from.

**3. The need for private events** (3,000). What an event is. Who publishes and who consumes: autonomous agents, smart contracts,
wallets, applications. What public events leak (who reacted, when, to what; interest; relationships). Concrete scenarios. Why existing
Midnight mechanisms (public events, indexer subscriptions, wallet scanning) do not meet the need. What would be lost without a private
event bus.

**4. Defining private events** (4,500). The definition: terms (event, envelope, shard, tag, publisher, subscriber, consumer, operator);
the named privacy properties; the adversary classes (single relay, indexer, chain observer, colluding minority, global observer); a
leakage table stating what each adversary learns; the explicit non-claims; the limits from the literature that bound what can be
claimed (anonymity trilemma, anonymity of gossip, the cost of receiver privacy, forward secrecy and deniability gaps). End the body of the chapter with the
precise, short definition the rest of the document uses. The chapter then closes with a formal Midnight Problem Statement (the private-events MPS (MPS-xxxx), written separately in the Foundation's MPS format and appended by the build); do not write it, and end your text with a sentence that the chapter closes with that problem statement.

## Part II. Options and requirements

**5. Prior art and the design space** (4,500). A taxonomy, not a survey of everything: Bitmessage and what it taught; the lineage of
metadata-private messaging (DC-nets, mixnets, private information retrieval); receiver privacy (fuzzy detection, oblivious retrieval);
decentralized publish/subscribe overlays and GossipSub; deployed messengers; ledger-based message carriers and stealth addressing.
For each family: mechanism, what it hides, what it costs, where it fails, and what it implies for Midnight. A comparison table.

**6. Architecture options for Midnight** (4,500). Five options, evaluated against the same criteria, stated at the start of the chapter with their source (the privacy properties and adversaries of Chapter 4 and the ten decision areas: format, privacy definition, publish/subscribe model, sustainability, performance, storage, operators, network tether, threats, verification). The options are judged before the detailed requirements of Chapter 7 exist, so the criteria must be stated in Chapter 6 and not borrowed from Chapter 7:
Option 1 *Ledger and indexer only*; Option 2 *Hybrid: GossipSub sidecar overlay with ledger anchoring* (recommended);
Option 3 *In-node protocol* (extend or fork the Midnight node); Option 4 *Mix-network or PIR-based delivery*;
Option 5 *External pub/sub service* (federated brokers or a Nostr/Waku-style relay network). Criteria: privacy properties delivered,
fit with Midnight today, performance, storage, operator burden and incentives, upgrade path, risk. Recommendation, fallback and the
conditions that would change the choice.

**7. Analysis of the requirements** (5,500). How the requirements are organized (ten decision areas, twelve requirement areas); the
shape of the requirement set (counts by area, scope, priority); the decisions that shape everything else and how they were resolved
(the decision register, grouped); the parameters and the arithmetic behind the main ones (envelope sizes, load, bandwidth, storage,
timing chains); the conflicts found between requirement areas and their resolution; the decisions that remain open and what would
settle each. Include a section "Threats and defences" (decision area D9, requirement area SEC): the attacks that matter (eclipse, Sybil, spam and storage exhaustion, replay, censorship by operators, traffic analysis, key compromise, indexer abuse, malicious contracts), the defence the requirements provide against each, the residual risk, and the attacks the design does not stop. Points to Appendix A.

## Part III. Experimental design for Private Events using GossipSub

**8. The reference system** (4,500). The system under test: components (Bus Node, Store Node, client library, anchoring, mock ledger and
indexer), the envelope and sealing scheme with byte layout, tags and recognition, the admission mechanism and its stand-in, the
GossipSub v1.2 configuration (topics per shard, mesh parameters, validation, scoring, message identifier), storage and back-fill, anchors
and contract consumption, the ledger-only fallback. Diagrams. What is real and what is mocked, stated plainly.

**9. Experimental design** (5,000). The questions the experiments answer (the seventeen open questions), each with its hypothesis, the
scenario and metric that test it, and the result that would change the design. The ten standard scenarios and the harness that runs
them (real swarms in one process, seeded schedules), the metrics and how each is measured, the pass criteria, controls and variant
runs, how results are checked (isolated runs, repeated seeds, attribution of delivery to the gossip path versus repair), threats to
validity, and what the setup cannot show.

**10. Pilot results and what they change** (5,000). What three independent implementations of the same specification showed. Results by
question and scenario with the measured numbers; where the expected result held and where it did not; the findings that change
requirements and parameters (tables); what remains unknown. Honest limits: one machine, in-memory networking, a stand-in admission proof.

**11. Open questions, roadmap and risks** (2,500). The next experiments, in order, with the evidence each needs; the phased plan from
prototype to production; operator and governance questions; the main risks and what would make the team change course.

**12. Conclusion** (1,000). What is decided, what is recommended, what is open.

## Final section
- **Midnight Improvement Proposal** ("Midnight Express", MIP-xxxx, the last section of the document, after the appendices): the specification of the private event bus in the Foundation's MIP format. See MIP_BRIEF.md.

## Back matter
- **References** (generated from the citations in the text).
- **Appendix A. Requirements in EARS form.** Every requirement derived: parameters, then the twelve areas (generated from the
  requirement set).
- **Appendix B. Annotated reading list.** About 100 works, grouped by theme, each with a short annotation: what it is, what it shows,
  how it bears on this design and any caveat.

## Chapter ownership for drafting
| Writer | Chapters | Reading-list themes |
|---|---|---|
| W1 | 1, 2, 3, 4 | Foundations: Bitmessage and its heirs; definitions, bounds and surveys |
| W2 | 5, 6, 7 | Design space: overlays, content-based pub/sub, ledger carriers, messengers, mix-nets and PIR |
| W3 | 8, 9, 11 | Network and experiment: GossipSub and libp2p, source anonymity and spam, Midnight and IOG networking |
| W4 | 10, 12 (and the executive summary after the others are drafted) | Cryptography and consumers: receiver privacy, sessions and groups, post-quantum, edge and IoT |
