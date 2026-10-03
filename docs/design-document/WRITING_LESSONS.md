# Writing lessons for the Midnight Express design document

This guide is for editors of "Midnight Express: Private Events for Midnight". It sits beside STYLE.md, which stays binding; where the two differ, STYLE.md wins. Section 1 catalogues the patterns that make prose read as machine-written, each with a test and a repair. Section 2 covers headings. Section 3 covers the shape of paragraphs and sections. Section 4 lists thirty checks a script can count. Section 5 lists the sources.

## What the evidence says

Readers like ours can tell. Russell, Karpinska and Iyyer hired annotators to label 300 non-fiction articles as human or machine-written. Annotators who rarely used LLMs did little better than chance and were overconfident. Five annotators who used LLMs often for writing reached a true positive rate of 92.7 percent with a false positive rate of 3.3 percent on GPT-4o articles, and their majority vote misclassified 1 article of 300, beating most commercial detectors, including on paraphrased and "humanized" text. The engineers and researchers who will read this document use these tools every day. They are the expert population.

What the experts noticed, in order of frequency: vocabulary (53.1 percent of explanations), sentence structure such as "not only ... but also" and lists of exactly three (35.9 percent), grammar and punctuation (24.8 percent), lack of originality (23.7 percent), quotes (22.3 percent) and clarity, meaning over-explanation (19.5 percent). Humanization lowered their confidence but did not remove the clues.

The vocabulary signal is measurable at population scale. Kobak and colleagues found that at least 13.5 percent of 2024 PubMed abstracts went through an LLM, on the evidence of excess style words: "delves" appeared 28 times more often than expected, "underscores" 13.8 times, "showcasing" 10.7 times, and common words such as "potential", "findings" and "crucial" rose by several percentage points. Of the 379 excess style words in 2024, 66 percent were verbs and 14 percent adjectives. Juzek and Ward isolated 21 focal words ("delves" up 6,697 percent between 2020 and 2024, "showcasing" 1,396 percent, "underscores" 904 percent, "intricate" 611 percent, "realm" 381 percent, "aligns" 267 percent) and found evidence consistent with preference tuning as a cause. Liang and colleagues saw "commendable", "meticulous" and "intricate" rise 9.8, 34.7 and 11.2-fold in ICLR 2024 peer reviews.

Removing words does not remove the fingerprint. Reinhart and colleagues (PNAS, 2025) compared human and model text on Biber's grammatical features. Instruction-tuned models used present participial clauses at 2 to 5 times the human rate (GPT-4o at 5.3 times), nominalizations at 1.5 to 2 times, more "that" clauses as subjects and more phrasal coordination, and used the agentless passive at about half the human rate. Sun and colleagues showed that a classifier can tell five commercial models apart with 97.1 percent accuracy and that the signal survives rewriting by another model, because it lives partly in what the text chooses to say. Content choices matter as much as surface edits: a sentence that names a number, a mechanism and a source carries less model signal than any rephrasing of a generic one.

Long technical documents fail at the level of structure. Oh and colleagues built six measures of "scientific slop" over 390 paired papers: sections no other section refers to, later sections that repeat earlier ones, claims that appear before their support, citations with no stated role, method figures that hide the method, and papers with no concrete example. The measures identified the machine-written paper in each pair 85.9 percent of the time (a token-based detector managed 68.7 percent), and higher scores went with lower ICLR ratings. Revision aimed directly at the measures overcorrected, pushing scores past human levels. Over-scrubbed prose is also a pattern.

What readers dislike, when asked: Shaib and colleagues interviewed writers, journalists and NLP researchers and annotated "slop" at span level. Verbosity was the indicator annotators agreed on; low density, poor relevance, repetition, templated structure and tone also predicted the label. Russell's experts called machine prose "safe" and boring.

Two cautions. Detectors have non-trivial error rates and break under paraphrase (Wikipedia, "Signs of AI writing", caveats), so a passing detector score proves nothing. And single features are weak: one Foundation proposal (MIP-0002) uses 13.7 em dashes per 1,000 words. Editors should look for clusters, then fix the cluster.

## 1. The pattern catalogue

Each entry gives a test an editor can apply to a sentence or paragraph, a bad example and a repair. Repairs use the facts in FACTS.md; never introduce a number or name that is not in the document's sources. When the repair needs a fact the text does not have, cut the sentence.

### Vocabulary

#### 1.1 Stock vocabulary

Test: the word appears in the banned list of Section 4 (C3), or it could be deleted or replaced by a plainer word with no loss of meaning.

Bad:

> The Bus Registry plays a pivotal role in fostering a robust and trustworthy overlay, underscoring Midnight's commitment to privacy.

Repaired:

> The Bus Registry is a Compact contract. It holds the Bus Operators' bonds and the membership and quota roots that Bus Nodes check when they admit an Envelope.

#### 1.2 Inflated significance

Test: the sentence says that something marks, represents, reflects or shapes something larger, and the larger thing is not the subject of the paragraph.

Bad:

> The introduction of contract events in MIP-0002 marks a pivotal moment in Midnight's evolution, setting the stage for a new era of privacy-preserving applications.

Repaired:

> MIP-0002 lets a Compact circuit emit an event with a 32-byte name and a 256-byte payload. All fields are public, and the virtual machine drops any event above 1 KiB without an error.

#### 1.3 Promotional adjectives

Test: the adjective praises (powerful, elegant, novel, efficient, lightweight, flexible, scalable) and no measurement in the same paragraph supports it.

Bad:

> Recognition Tags offer an elegant and highly efficient way for Subscribers to find their Messages.

Repaired:

> A Subscriber recognizes its Messages by recomputing a salted 16-byte Recognition Tag for each key it holds, which costs 0.2 to 0.5 microseconds per key.

#### 1.4 Sincerity markers and second-order substitutes

Test: a word claims candour or precision instead of supplying it ("plainly", "honestly", "genuinely", "frankly", "to be clear", "explicitly", "squarely", "the honest answer"). These words multiply once the first-order list is banned; "stated plainly" and "the price of" are the substitutes this document has already grown.

Bad:

> The stand-in, stated plainly, is not secure. That is the price of shipping a prototype.

Repaired:

> The prototype's admission proof is a stand-in whose secrets every relay can read. It is acceptable on devnet and testnet only; the production proof system is chosen by a follow-up proposal.

#### 1.5 Vague attribution

Test: an opinion or finding is credited to "experts", "researchers", "the literature", "many" or "studies" and the sentence has no citation key.

Bad:

> Researchers have long noted that peer scoring cannot stop Sybil attacks.

Repaired:

> The Least Authority audit of GossipSub v1.1 found that peer scoring is not a complete Sybil defence [@2020-leastauthority-gossipsub-audit].

Use only keys from build/bibkeys.txt. If no source in that list supports the claim, cut the sentence.

#### 1.6 Pet metaphors

Test: a figure of speech stands where a mechanism should be (safety net, backbone, cornerstone, gatekeeper, bridge, lens, heart, double-edged, the price of, a trade-off "at the heart of"). Count each metaphor frame across the chapter; a frame used twice is a tic.

Bad:

> The ledger lane acts as a safety net, catching Messages that fall through the cracks of the overlay.

Repaired:

> When the overlay fails to deliver, a Publisher can post the sealed Envelope through the ledger lane. Delivery then takes 25 to 36 s at the 99th percentile, and the whole chain carries about 6.3 class-1 Messages per second.

### Sentence constructions

#### 1.7 Negative parallelism

Test: the sentence denies something no one claimed before stating the real point ("not only X but also Y", "not X, but Y", "is not X; it is Y", "Y rather than X", "no X, no Y, just Z").

Bad:

> Midnight Express is not just a transport; it is a new privacy layer for the entire ecosystem.

Repaired:

> Midnight Express carries sealed Messages between Publishers and Subscribers over GossipSub and anchors a digest of each 60-second window on the ledger.

Keep a contrast when a named reader would otherwise draw the wrong conclusion. STYLE.md requires one: Midnight Express complements on-chain private events and does not replace MPS-0005 Part 2.

#### 1.8 Rule of three

Test: three parallel items where the content has two, four or one, or three abstract nouns or adjectives in a row ("secure, scalable and sustainable").

Bad:

> The design is private, performant and practical, giving builders flexibility, reliability and peace of mind.

Repaired:

> The design hides Message content and Subscriber interest from relays. It does not hide timing or who talks to whom.

Lists of three are fine when there are three things: three size classes would be three, and there are four.

#### 1.9 Participial tails

Test: the sentence ends with ", ensuring ...", ", enabling ...", ", making ...", ", highlighting ..." or ", thereby ...", and the tail asserts a benefit or significance that no measurement supports. Reinhart and colleagues measured these clauses at up to 5.3 times the human rate.

Bad:

> Each Bus Node sends IDONTWANT for large Envelopes, significantly reducing bandwidth and ensuring a smooth experience for operators.

Repaired:

> With IDONTWANT enabled, a Bus Node tells its mesh peers not to send an Envelope it already holds. In the pilot this cut median ingress amplification from about 5.1x to about 2.3x and class-3 egress by 70 to 76 percent.

#### 1.10 Copula avoidance

Test: "serves as", "stands as", "acts as", "functions as", "represents", "features", "offers" or "boasts" where "is" or "has" would do.

Bad:

> The Anchor serves as a commitment to the window's Envelopes and features a Merkle root over every Shard.

Repaired:

> The Anchor is a ledger record that commits to every Envelope accepted in one 60-second window, across all Shards.

#### 1.11 False ranges

Test: "from X to Y" where X and Y are not two ends of one scale.

Bad:

> Midnight Express serves everyone from autonomous agents to institutional wallets, from games to decentralized finance.

Repaired:

> Chapter 3 works through four cases: agents trading in a shared world, a payment that needs a message, a contract that must tell a holder something, and a group alert feed.

A true range has units: "wire lengths from 776 B to 16,904 B".

#### 1.12 Synonym cycling

Test: one thing is called by two or more names within a section (Bus Node, relay, peer, node, router). The glossary in STYLE.md fixes one name per thing; synonym cycling breaks it and reads as a repetition penalty at work.

Bad:

> A Bus Node validates each Envelope. If the relay rejects it, the peer's score falls, and the router may prune the node from its mesh.

Repaired:

> A Bus Node validates each Envelope. A Reject lowers the sending Bus Node's score, and a Bus Node with a negative score is pruned from the mesh at the next heartbeat.

"Relay" may still describe a role ("a Bus Node relaying for a Shard it does not subscribe to"), never replace the term.

#### 1.13 Stacked hedges

Test: two hedges qualify one claim ("may potentially", "could possibly", "might arguably", "likely somewhat"). Uncertainty belongs in the evidence, not the modal verbs.

Bad:

> The restart barrier may potentially cause some delivery delays in certain churn scenarios.

Repaired:

> During the 140 s restart barrier, a Bus Node that silently ignored Envelopes left the 99th-percentile delivery at 42.7 s (or delivered 81.6 percent); an explicit Busy reply gave 100 percent delivery at 1.1 s.

One hedge with its reason is fine: "The result may not hold at 1,000 nodes; the pilot ran 50 on one machine."

#### 1.14 Nominalization stacks

Test: the action of the sentence sits in a noun ("the enforcement of", "the verification of", "performs the validation of") and the verb is weak (is, performs, provides, enables). Gopen and Swan's fifth principle: put the action in the verb.

Bad:

> The enforcement of per-membership quotas is performed through the verification of admission nullifiers by each Bus Node.

Repaired:

> Each Bus Node enforces its own per-membership quota by checking the admission nullifier in each Envelope against those it has already seen in the current admission window.

#### 1.15 Staccato punchlines and aphorisms

Test: a run of two or more short sentences that land a slogan, or a sentence of the form "X is the Y of Z". One short sentence for a claim is good; a run of them is theatre.

Bad:

> Scoring is not enough. Sybils adapt. Bandwidth is the real currency of the mesh.

Repaired:

> Peer scoring slows a Sybil attacker but does not stop one [@2020-leastauthority-gossipsub-audit]. Bonds held in the Bus Registry raise the cost of each identity.

#### 1.16 Rhetorical questions and staged run-ups

Test: the text asks a question it answers in the next sentence, or opens with "Here's the thing", "The answer is simple", "Consider the following".

Bad:

> So why not simply put the Messages on chain? The answer is simple: cost.

Repaired:

> The ledger lane carries about 6.3 class-1 Messages per second for the whole chain, because `bytes_written` limits each block to 50,000 B. One Shard at its limit of 10 class-1 Envelopes per second would exceed it.

Questions are allowed where they are the content: the seventeen open questions of Chapter 9, the Open Questions of the problem statement.

#### 1.17 Arguing with no one

Test: the text corrects a misconception that no source, reader or earlier chapter has stated ("This is not a mixnet", "Contrary to what one might expect").

Bad:

> Contrary to popular belief, GossipSub is not anonymous.

Repaired:

> GossipSub has no anonymity mechanism. A Bus Node that receives an Envelope straight from a Publisher sees the Publisher's network address, and any relay can estimate its distance from the Publisher by reaction time, which the protocol "does not try to obscure" [@2020-leastauthority-gossipsub-audit, p. 7].

#### 1.18 Colon reveals

Test: a short noun phrase, a colon and the payoff ("The result: ...", "The catch: ...", "The lesson: ...", "The upshot is: ...").

Bad:

> The catch: independent validators cannot see each other's state.

Repaired:

> Independent validators cannot see each other's state, so a network-wide quota cannot be enforced: in the pilot, 2 of 2 and 5 of 5 conflicting Envelopes were accepted.

#### 1.19 Filler phrases

Test: the phrase can be cut or shortened without changing meaning ("in order to", "it is important to note that", "it is worth noting", "due to the fact that", "has the ability to", "in the context of", "a wide range of", "when it comes to").

Bad:

> It is worth noting that, in order to reduce load, Store Nodes have the ability to drop Envelopes older than 48 hours.

Repaired:

> Store Nodes drop Envelopes after 48 hours (172,800 s) unless the Publisher paid for the 7-day archive.

#### 1.20 Repeated sentence openings

Test: three consecutive sentences start with the same word or the same subject-verb pair.

Bad:

> The Publisher seals the Message. The Publisher then computes the Recognition Tag. The Publisher attaches the admission proof. The Publisher submits the Envelope.

Repaired:

> The Publisher seals the Message, computes its Recognition Tag and fills the 512-byte admission slot. The finished Envelope goes to any Bus Node on the Shard.

#### 1.21 Writing about the document

Test: the sentence describes the text ("This section explores", "The table below compares", "As discussed above", "We now turn to") instead of the subject. Outside the Chapter 1 roadmap, cut it or turn it into a claim.

Bad:

> This section takes a closer look at how the Store Node handles back-fill, which will be explored further in Chapter 9.

Repaired:

> A Subscriber that was offline asks a Store Node for the Envelopes it missed on its Shard, and the Store Node answers from its 48-hour window.

The sentence that introduces a table (required by STYLE.md) states what the table shows, not that a table follows: "Adversary classes differ in what they learn about Subscriber interest."

#### 1.22 Provenance and history

Test: the text narrates how it was produced or what changed ("an earlier draft", "was renamed", "we fetched", "unverified", "the reviewers asked", implementation labels such as g1). STYLE.md forbids all of it.

Bad:

> The message identifier was revised after an earlier version used the envelope identifier, which g1 had proposed.

Repaired:

> The GossipSub message identifier is a hash of all wire bytes. The envelope identifier, which excludes the admission slot, is used for deduplication, admission binding and Anchors.

### Paragraph shape

#### 1.23 Summary closers

Test: the last sentence of a paragraph restates the paragraph ("In short", "Overall", "In other words", "This means", "This is why", "Taken together"). Wikipedia files these under section summaries.

Bad:

> Each Shard carries at most 10 Envelopes per second and 64 KiB per second, whichever binds first. A Bus Node at D = 8 forwards each Envelope to eight mesh peers. In short, the load per Shard is bounded and predictable.

Repaired:

> Each Shard carries at most 10 Envelopes per second and 64 KiB per second, whichever binds first. A Bus Node at D = 8 forwards each Envelope to eight mesh peers, so one Shard at its byte limit costs it at most 8 x 64 KiB/s = 512 KiB/s of egress, about 4.2 Mbit/s against the 6 Mbit/s edge budget.

#### 1.24 Demonstrative closers

Test: the last sentence starts with "This", "That" or "These" plus a weak verb and draws a moral ("That is the price of ...", "This is why ...", "This keeps ..."). Allow one per chapter where the moral is a decision the reader needs.

Bad:

> Every Envelope pays 512 bytes for the admission slot even when the proof is smaller. That is the price of a constant-size slot.

Repaired:

> Every Envelope carries a 512-byte admission slot whatever the size of the proof, so each size class has exactly one wire length. A class-0 Envelope therefore spends 690 of its 776 wire bytes on overhead and carries 86 bytes of payload.

#### 1.25 Heading echo

Test: the first sentence after a heading restates the heading ("## Peer scoring" followed by "Peer scoring is an important part of GossipSub").

Bad:

> ## Peer scoring
>
> Peer scoring plays a key role in the security of the overlay.

Repaired:

> ## Peer scoring
>
> Each Bus Node keeps a score for every peer, built from time in the mesh, first deliveries, mesh delivery rate and invalid Messages, and stops gossiping to peers whose score falls below the gossip threshold.

#### 1.26 The challenges-and-outlook formula

Test: a paragraph or section of the form "Despite X, Y faces several challenges. ... Despite these challenges, Y is well placed to ...".

Bad:

> Despite its strengths, Midnight Express faces several challenges, including operator incentives and proof costs. Nevertheless, with continued research, these hurdles can be overcome.

Repaired:

> Two questions decide whether Midnight Express can leave testnet. No proof system has yet shown a verification cost near the 4.5 ms per proof that the pilot assumed. And DUST cannot be transferred, so paying Bus Operators needs NIGHT or another mechanism that the design has not chosen.

#### 1.27 Cheerleading endings

Test: the paragraph or chapter ends on promise, excitement or reassurance ("paves the way", "opens exciting possibilities", "the future is bright", "well positioned").

Bad:

> With these results, Midnight Express is well positioned to become the foundation for private communication on Midnight.

Repaired:

> The pilot ran 50 Bus Nodes on one machine with in-memory networking and a stand-in admission proof. Every number in this chapter carries those limits.

#### 1.28 Repetition across chapters

Test: a paragraph restates a point owned by another chapter, with the same numbers. Oh and colleagues measure this as macro redundancy. Refer instead.

Bad (in Chapter 11):

> As shown earlier, IDONTWANT reduces median ingress amplification from 5.1x to 2.3x, and an explicit Busy reply improves delivery during restarts, which demonstrates that the design is sound.

Repaired:

> The next experiment repeats the IDONTWANT runs across several machines, because the result in Chapter 10 comes from one process.

#### 1.29 Citation without a role

Test: a citation key that the sentence does not use: the sentence does not say what the work showed, built or measured, or how this design differs from it.

Bad:

> Many systems address metadata privacy [@2017-piotrowska-loopix; @2017-chaum-cmix; @2017-alexopoulos-mcmix; @2019-leibowitz-silentmixes].

Repaired:

> Loopix hides who talks to whom with mixing and cover traffic, at the cost of added latency at every hop and constant traffic from every client [@2017-piotrowska-loopix]. Midnight Express does not attempt relationship privacy at launch.

#### 1.30 Claim before support

Test: a judgement ("is the strongest option", "is impractical") appears a paragraph or more before the facts that justify it, or never meets them. Lamport's rule applies to the whole document: state the problem and the correctness conditions before the solution.

Bad:

> Option 4 is impractical for Midnight. Mix networks have been studied for decades and offer strong guarantees.

Repaired:

> A mix network delays each Message at every hop and needs cover traffic from every client to hide Subscriber interest. Against the Chapter 6 criteria, that rules Option 4 out for interactive use at launch.

### Tone

#### 1.31 Overcorrection

Test: the scrubbed text has acquired its own uniformity: every sentence short, every passive turned active even where the agent is irrelevant, hedges removed where uncertainty is real, glossary terms swapped for variety. Reinhart and colleagues found human text uses the agentless passive about twice as often as GPT-4o; Wikipedia lists plain hedges ("perhaps", "tends to") as more common in human writing.

Bad (overcorrected):

> The validator checks the slot. The validator checks the nullifier. The validator rejects bad Envelopes. The design works.

Repaired:

> An Envelope whose admission proof fails is rejected, and the rejection counts against the score of the Bus Node that forwarded it. Whether the check stays within budget under a production proof system is open.

### Formatting

#### 1.32 Bullets where prose belongs

Test: a list whose items depend on each other (because, so, unless), or items longer than about 40 words, or a list of two. Lists are for parallel, independent items (STYLE.md). A bulleted argument drops the connectives (because, so, unless) that carry it.

Bad:

> - IDONTWANT reduces amplification.
> - Therefore class-3 egress falls.
> - This makes the 6 Mbit/s budget achievable.

Repaired:

> IDONTWANT cut median ingress amplification from about 5.1x to about 2.3x, and with it class-3 egress fell by 70 to 76 percent.

#### 1.33 Bold run-in lists and decorative emphasis

Test: list items that open with a bold label and a colon, or bold or italic used for emphasis inside a sentence. Bold is for requirement identifiers in Appendix A, figure captions and a glossary term at its single defining use.

Bad:

> - **Confidentiality:** Content is **fully encrypted** end to end.
> - **Interest privacy:** Relays **cannot** learn what Subscribers want.

Repaired:

> A relay sees a sealed Envelope and a Recognition Tag salted for that Envelope, so it cannot read the content or match the Message to a Subscriber from the Tag alone. It does see the size class, the timing and the Shard.

Run-in labels are acceptable where every item is judged against the same named criteria and the reader compares across items, as in the option evaluations of Chapter 6. Use them nowhere else.

#### 1.34 Dashes

Test: any em dash, any spaced en dash and any double hyphen used as a dash. STYLE.md bans em dashes; use a comma, colon, parentheses or a full stop. Write ranges with "to".

Bad (dashes shown as `--`):

> The Busy reply -- sent during the 140 s barrier -- tells the Publisher to retry elsewhere -- no silent loss.

Repaired:

> During the 140 s restart barrier a Bus Node answers with Busy, and the Publisher retries at another Bus Node.

#### 1.35 Small tables that should be sentences, and typographic residue

Test: a table of two rows or two columns that a sentence would carry; curly quotes in the Markdown source; emoji; horizontal rules between sections.

Bad:

> | Parameter | Value |
> |---|---|
> | Heartbeat | 1 s |

Repaired:

> The heartbeat interval is 1 s.

## 2. Headings

A heading names what the section holds or states what it found. It does not announce, tease, ask or sell. The text must still make sense if every heading is removed (Knuth's rule from the Stanford mathematical writing course): the first sentence after a heading repeats the subject in words, never as "This" or "It".

### Rules

1. Sentence case. Capitalize the first word, proper nouns, glossary terms (Bus Node, Store Node, Shard, Recognition Tag, Bus Registry, Anchor) and protocol names (GossipSub, IDONTWANT). Google, Microsoft and Wikipedia's Manual of Style all require it. RFCs and PEPs use title case by house rule, so title case alone proves nothing; mixed case in one document does.
2. Name the thing in descriptive chapters. A noun phrase that names the object or mechanism: "The envelope", "Router settings", "Restart barrier and the Busy reply".
3. State the finding in results chapters. In Chapter 10, and wherever a section exists to report one result, the heading is the result in a few words: "IDONTWANT is the largest cost lever". A claim heading must be true of everything under it.
4. One form per level within a chapter. Microsoft asks for parallel structure at each level. Chapter 10's "Results by question" mixes claims ("IDONTWANT is the largest cost lever", "Admission: local quotas hold, a network-wide quota does not") with bare labels ("Message identifier", "Recognition cost"); pick claims for all of them.
5. No announcing verbs or gerund openers ("Understanding", "Exploring", "Navigating", "Unpacking", "A closer look at"). Google asks for noun phrases in conceptual headings and avoids "-ing" first words; "Binding the visible header" becomes "Visible-header binding" or "How the visible header is bound to the slot".
6. No stock headings: "Overview", "Background", "Key takeaways", "Summary", "Final thoughts", "Challenges and future directions", "Why it matters", "Putting it all together". The only "Introduction" is Chapter 1, the only "Conclusion" is Chapter 12, and the MIP and MPS keep their template words.
7. No "The role of X", "The importance of X", "The power of X", "The future of X".
8. No question headings (Wikipedia's Manual of Style; Microsoft allows them only where needed for meaning). The MPS heading "Open Questions" is fixed by the template.
9. No colon slogans ("Deep dive: the envelope", "Admission: ensuring fair access"). A colon is allowed in "Option 3: In-node protocol" and in the problem statement's title.
10. No metaphor, no adjectives of praise, no "stated plainly", no ending punctuation, no links, no bold or italics. Code in a heading needs a noun beside it ("The `Misc` event name").
11. No heading for a section under about 120 words, no single subsection under a section (Microsoft: if there are not two distinct topics, skip the subheadings), no two headings without text between them (Google, Microsoft). The MIP's "Path to Active" gets one sentence before "Acceptance Criteria".
12. Do not repeat the parent heading's words (Wikipedia: "Early life", not "Smith's early life"). Under "## Admission", write "### What a relay checks", not "### Admission checks performed by relays".
13. Keep headings short: eight words at most, the important word first.
14. Unique headings within the document, so that cross-references and the table of contents work.

### Twenty-five bad headings and their repairs

| # | Bad heading | What is wrong | Repair |
|---|---|---|---|
| 1 | Understanding Midnight's Event Model | Gerund announce, title case | What the chain offers for events |
| 2 | The Role of GossipSub in Midnight Express | "The role of", title case | GossipSub v1.2 between Bus Nodes |
| 3 | Key Takeaways | Stock heading, recap | (delete; end the chapter on its last finding) |
| 4 | Conclusion (inside Chapter 8) | Section summary | (delete; Chapter 12 is the only conclusion) |
| 5 | Navigating the Privacy-Performance Trade-off | Gerund, metaphor | Padding cost of the four size classes |
| 6 | Why Does Privacy Matter? | Question, vague | What public events leak |
| 7 | Admission: Ensuring Fair Access | Colon slogan, participle, promise | Per-membership admission quotas |
| 8 | Security, Scalability, and Sustainability | Triad, three topics under one heading | Operator cost at one Shard (and separate sections for the others) |
| 9 | Overview | Stock, says nothing | Components |
| 10 | Deep Dive: The Envelope Format | Colon slogan, title case | Envelope byte layout |
| 11 | A Closer Look at Recognition Tags | Announces | Recognition Tags and matching cost |
| 12 | Putting It All Together | Stock, announces synthesis | The life of one Event |
| 13 | Challenges and Future Directions | AI outline formula | Main risks and what would change course |
| 14 | How It Works | Pronoun, vague | Admission check at a Bus Node |
| 15 | Mesh Parameters | Title case | Mesh parameters |
| 16 | Introduction to Store Nodes | Announces | Store Nodes and back-fill |
| 17 | Storage Considerations | Empty noun "considerations" | Retention and back-fill |
| 18 | Leveraging IDONTWANT for Efficiency | Banned verb, gerund, vague benefit | IDONTWANT cuts ingress amplification from 5.1x to 2.3x |
| 19 | The Ledger Lane: A Safety Net | Colon, metaphor | The ledger lane |
| 20 | Threat Landscape | Banned word | Threats and defences |
| 21 | What You Need to Know About Nullifiers | Addresses the reader, bare "nullifier" | Admission and consumption nullifiers |
| 22 | Busy Replies: Not Just a Status Code | Negative parallelism, colon | The Busy reply during the restart barrier |
| 23 | Final Thoughts on Operator Incentives | Stock, recap | Who pays Bus Operators |
| 24 | Phase 1: Devnet Rollout | "Phase" belongs to MPS-0005; colon | Stage 0 on devnet |
| 25 | The Stand-in, Stated Plainly | Sincerity marker | The stand-in admission proof |

### Heading rules for this document's structure

The build numbers chapters; never number a heading by hand.

Parts are front-matter dividers with fixed titles from OUTLINE.md: "Part I. Midnight and the case for private events", "Part II. Options and requirements", "Part III. Experimental design for Private Events using GossipSub". The form is "Part" plus a Roman numeral, a full stop and a sentence-case title. Part III's capitalized "Private Events" breaks the sentence case of the other two; raise it with the owner rather than changing it.

Chapters use one `#` with an anchor: `# Midnight in brief {#ch2}`. Titles come from OUTLINE.md. Descriptive chapters take noun phrases; Chapter 10's title is already a claim about what the results change, which suits a results chapter.

Sections use `##` and subsections `###`. Do not go below `###` in Chapters 1 to 12. Within one chapter, all `##` headings take the same form (all noun phrases or all claims), and so do all `###` headings under one `##`. The option sections of Chapter 6 keep the "Option N: name" form for all five.

Appendices use `# Appendix A. Requirements in EARS form {#appendix-a}` and `# Appendix B. Annotated reading list`: "Appendix", a capital letter, a full stop, a sentence-case title. Appendix A's area headings name the area ("Envelope format", "Cryptography"), not the prefix alone.

The References heading is `# References {.unnumbered #references}` and nothing else.

The problem statement that closes Chapter 4 follows the Foundation's MPS template. Its headings are fixed and stay in the template's title case: Abstract, Vision, Problem, Use Cases, Goals, Expected Outcomes, Open Questions, Recommended MIPs, References, Acknowledgements, Copyright. They sit one level below "### Midnight Problem Statement: Private Events". Do not add, rename, reorder or recase them.

The Midnight Improvement Proposal at the end of the document follows the Foundation's MIP template, which says "The headings in this template are part of the structure." Its `##` headings are fixed, in this order and this case: Abstract; Motivation; Specification; Rationale; Path to Active (with `###` Acceptance Criteria and `###` Implementation Plan); Backwards Compatibility Assessment; Security Considerations; Implementation; Testing; References; Acknowledgements; Copyright Waiver. MIP_BRIEF.md drops the template's "(Optional)" from References, as MIP-0002 does. Do not change any of these. The Specification's `###` subsections are also fixed by MIP_BRIEF.md and use sentence case: Terminology and conventions; Event envelope and sealing; Overlay protocol; Ledger interface; Consumer interface; Versioning. Below them, `####` headings name protocol objects and procedures ("Message identifier", "Validation outcomes", "Anchor record layout"), never claims, because a specification describes behaviour rather than arguing for it. The rules above apply to everything a writer adds; the template's own words are exempt from rules 1, 6 and 8.

## 3. Paragraph and section shape

1. Open with the subject and the claim. Google's technical writing course calls the opening sentence the most important in the paragraph, because busy readers skim openings. Gopen and Swan's topic position: put the thing whose story the sentence tells first, and link backward to what the reader already has.
2. End on the newest fact. The stress position at the end of a sentence and of a paragraph is where readers look for what matters (Gopen and Swan). The last sentence of a paragraph carries the number, the consequence for the design or the requirement identifier, never a restatement.
3. One topic per paragraph. Google's rule: a paragraph is an independent unit of logic; delete or move any sentence that describes a past or future topic.
4. Let length follow content. A paragraph that carries one fact is one or two sentences; a derivation can run to ten. The GossipSub v1.1 specification, a human-written protocol text, has a coefficient of variation of paragraph length of 1.21; the assembled draft of this document measures 0.69. Uniform paragraphs of four to five sentences are a template.
5. Vary sentence length on purpose. Short sentences carry claims, longer ones carry reasoning (STYLE.md). Knuth: read it aloud and change the wording if the rhythm is wrong. A run of four sentences of nearly equal length is a signal to merge two or split one.
6. Keep uncertainty exact. Say which of measured, derived or assumed a number is, under what conditions it was measured, and what would change it. One hedge with its reason beats three without. "Measured at 50 Bus Nodes on one machine; untested across machines" is exact. "May potentially vary in larger deployments" is not.
7. Define a term once, at first use, then use it unchanged. Knuth's rule 14: never use one notation for two things or two notations for one. The glossary in STYLE.md is the list of names.
8. Show the arithmetic for every derived figure where the figure first appears, and refer to that place afterwards.
9. Cite with a role. Every citation says what the work showed or how the design departs from it.
10. Put the problem and its correctness conditions before the solution (Lamport). Chapter 4 defines; Chapter 6 states its criteria before judging options; Chapter 8 describes the system against those definitions.
11. Do not recap. A section ends when its last fact is stated. A chapter ends on its last section's last fact. "In this chapter we have seen" never appears.

### Where signposting is allowed

Signposting means telling the reader what the text will do. It is allowed in these places only:

- The Chapter 1 roadmap: one paragraph, in the "Purpose" or "Scope" section, that names each part and chapter and what it decides. It is the only forward-looking description of the document's structure.
- The sentence before a table or figure, which STYLE.md requires; it states what the table shows ("Each adversary class learns a different subset of Envelope metadata"), not that a table follows.
- The closing sentence of Chapter 4's body, which OUTLINE.md requires, saying that the chapter closes with the problem statement.
- Cross-references that cite evidence, in the form of a citation: "Chapter 10 measures this at 2.3x" or "(`MPE-NET-012`)". A cross-reference names where the evidence or the owning requirement is; it never promises ("will be explored", "as we will see") or recalls ("as discussed above").

Everywhere else, remove sentences that describe the text, including paragraph-final pointers such as "The last section of this chapter lists both sides" and "The rest of the document does not claim more than Chapter 4 allows". If the second carries a real constraint, state it as one: "No later chapter claims a privacy property beyond those defined here."

### How sections end

A section ends on one of three things: its last fact, a decision with its identifier (`DEC-014`), or the consequence for the design ("so the Anchor must cover all Shards in one record"). It does not end on a summary, a moral, a forward pointer or a reassurance. A chapter ends the same way. The Executive summary and Chapter 12 are the only places that summarize, and both must add what the body does not say in one place: what is decided, what is recommended and what is open, with the numbers.

## 4. Mechanical checks

Run these on the Markdown source. Exclude fenced code, tables, YAML, figure captions, citation keys, footnote URLs, the References and Appendix A unless a check says otherwise, and quoted material. Regular expressions are Python `re` syntax. Counts are per chapter unless stated. A failed check is a prompt to read the sentence, not an automatic edit; the protocol and requirement vocabulary (key, honest node, critical path, harness) has technical senses that the checks allow.

C1. Em dashes. Count `\u2014` and a double hyphen used as a dash. Target 0.

```
\u2014|(?<=\w) -- (?=\w)
```

C2. En dashes. Count `\u2013` in prose. Target 0; write ranges as "10 to 15 s". Allowed in reference titles.

C3. Banned vocabulary. Target 0. The words: delve, tapestry, realm, landscape (abstract), underscore, showcase, pivotal, crucial, seamless, leverage, robust, intricate, intricacies, meticulous, commendable, testament, boast, garner, foster, vibrant, groundbreaking, cutting-edge, game-changer, holistic, multifaceted, synergy, paradigm shift, ever-evolving, unwavering, bolster, empower, elevate, streamline, revolutionize, state-of-the-art, invaluable, noteworthy, indelible, enduring.

```
(?i)\b(delv(?:e|es|ed|ing)|tapestry|realm|landscape|underscor(?:e|es|ed|ing)|showcas(?:e|es|ed|ing)|pivotal|crucial(?:ly)?|seamless(?:ly)?|leverag(?:e|es|ed|ing)|robust(?:ly|ness)?|intricac(?:y|ies)|intricate|meticulous(?:ly)?|commendable|testament|boast(?:s|ed|ing)?|garner(?:s|ed|ing)?|foster(?:s|ed|ing)?|vibrant|groundbreaking|cutting-edge|game-?changer|holistic|multifaceted|synerg(?:y|ies|istic)|paradigm shift|ever-evolving|unwavering|bolster(?:s|ed|ing)?|empower(?:s|ed|ing)?|elevat(?:e|es|ed|ing)|streamlin(?:e|es|ed|ing)|revolutioni[sz](?:e|es|ed|ing)|state-of-the-art|invaluable|noteworthy|indelible|enduring)\b
```

C4. Watch vocabulary. At most 2 per 1,000 words per chapter, each one replaceable only by a worse word. The words: key (as adjective of role, factor, insight, feature, benefit, challenge, finding), critical, essential, significant, comprehensive, nuanced, notable, notably, valuable, enhance, align with, navigate, ensure, facilitate, utilize, novel, powerful, elegant, innovative, fundamental, vital, insight.

```
(?i)\b(key (?:role|factor|insight|takeaway|feature|benefit|component|challenge|driver|consideration|aspect|element|point|question|difference|finding|advantage)s?|critical|essential|significant(?:ly)?|comprehensive|nuanced|notabl[ey]|valuable|enhanc(?:e|es|ed|ing|ement)|align(?:s|ed)? with|navigat(?:e|es|ed|ing)|ensur(?:e|es|ed|ing)|facilitat(?:e|es|ed|ing)|utili[sz](?:e|es|ed|ing|ation)|novel|powerful|elegant|innovative|fundamental(?:ly)?|vital|insights?)\b
```

C5. Banned phrases. Target 0.

```
(?i)\b(it is (?:important|worth|crucial) (?:to note|noting|to remember)|it should be noted|in order to|due to the fact that|the fact that|in today's|at its core|in essence|the heart of|plays? an? (?:\w+ )?role|a wide (?:range|array|variety) of|a (?:diverse|rich) (?:array|range)|when it comes to|in the realm of|in the context of|first and foremost|last but not least|needless to say|it goes without saying|serves? as a (?:reminder|testament)|stands? as a testament|has the ability to|is able to|at the end of the day|moving forward|going forward)\b
```

C6. Negative parallelism. At most 1 per chapter, and only where the text names who holds the mistaken view.

```
(?i)\bnot (?:only|just|merely|simply)\b[^.;]{0,80}\b(?:but|it is|it's)\b|\b(?:is|are|was|does|do) not (?:about )?[^.;]{1,60}[;,] (?:it|they|but) (?:is|are|does|do)\b|\bno [^.,;]{1,30}, no [^.,;]{1,30}, (?:just|only)\b
```

C7. "Rather than". At most 0.5 per 1,000 words; each one must contrast two real options.

```
(?i)\brather than\b
```

C8. Copula avoidance. Target 0 for "serves as", "stands as", "boasts", "features a", "offers a"; "acts as" and "functions as" at most 1 per chapter.

```
(?i)\b(serv(?:e|es|ed|ing) as|stand(?:s|ing)? as|act(?:s|ed|ing)? as|function(?:s|ed|ing)? as|operat(?:e|es|ed|ing) as|represent(?:s|ed)? an? |boasts?|features an?|offers an?)\b
```

C9. Participial tails. At most 1 per 1,000 words, and none that asserts a benefit without a number in the same sentence.

```
(?i),\s+(?:thereby\s+|thus\s+|further\s+)?(?:ensuring|enabling|allowing|making|providing|highlighting|underscoring|reflecting|demonstrating|showcasing|emphasizing|creating|offering|fostering|contributing|paving|setting|leading|resulting)\b[^.]*\.
```

C10. Triads. Abstract triads (three adjectives or abstract nouns) target 0; a paragraph with three or more triads of any kind is flagged.

```
abstract: (?i)\b(\w+(?:ive|al|ous|ble|ent|ant|ic|ful|less|ity|ness)), (\w+(?:ive|al|ous|ble|ent|ant|ic|ful|less|ity|ness)),? (?:and|or) (\w+(?:ive|al|ous|ble|ent|ant|ic|ful|less|ity|ness))\b
any:      \b[\w-]+(?: [\w-]+){0,2}, [\w-]+(?: [\w-]+){0,2},? (?:and|or) [\w-]+
```

C11. Stacked hedges. Target 0.

```
(?i)\b(may|might|could|possibly|potentially|perhaps|likely|arguably|somewhat|relatively|generally|typically|seemingly|presumably)\b(?:\W+\w+){0,5}?\W+(may|might|could|possibly|potentially|perhaps|likely|arguably|somewhat|relatively|seemingly|presumably)\b
```

C12. Intensifiers and sincerity markers. "Plainly", "honestly", "genuinely", "truly", "frankly", "to be clear" target 0 ("honest" as in honest node is fine); the rest at most 1 per 1,000 words.

```
(?i)\b(truly|genuinely|honestly|frankly|to be clear|really|very|extremely|incredibly|highly|deeply|plainly|simply|clearly|obviously|of course|indeed|crucially|importantly|interestingly|remarkably|undoubtedly|undeniably|absolutely|squarely)\b
```

C13. Unquantified comparatives. Target 0: any match in a sentence with no digit.

```
(?i)\b(significantly|substantially|dramatically|greatly|considerably|vastly|markedly|drastically)\s+(?:\w+\s+){0,2}?(reduc\w*|increas\w*|improv\w*|lower\w*|rais\w*|faster|slower|smaller|larger|better|worse|cheaper|higher)\b
```

C14. Vague attribution. Target 0 in sentences without `[@`.

```
(?i)\b(experts?|researchers|observers|critics|commentators|many|some|several) (?:\w+ )?(note|notes|argue|suggest|agree|believe|say|claim|have (?:shown|argued|noted))\b|\bit is (?:widely|generally|commonly) (?:accepted|believed|recognized|recognised|known)\b|\bstudies (?:show|have shown|suggest)\b
```

C15. Transition openers. At most 1 per 1,000 words.

```
(?m)(?:^|(?<=[.!?] ))(Additionally|Furthermore|Moreover|Notably|Importantly|Crucially|Consequently|Ultimately|Interestingly|Indeed|Overall|Essentially|Fundamentally),
```

C16. Repeated openings. Split paragraphs into sentences with `(?<=[.!?])\s+(?=[A-Z\x60(])`. Flag three consecutive sentences with the same first two words (target 0) and four with the same first word.

C17. Sentence-length variance. Over prose sentences of three or more words, compute the mean and standard deviation of word counts. Flag a chapter whose coefficient of variation (SD divided by mean) is below 0.5; the GossipSub v1.1 specification measures 0.59 and the current draft 0.65. Also flag any run of four consecutive sentences whose lengths all lie within 4 words of their own mean.

C18. Paragraph-length variance. Over prose paragraphs, flag a chapter whose coefficient of variation of paragraph length is below 0.6, and any run of five paragraphs within 20 percent of each other's length. Flag runs of three or more one-sentence paragraphs.

C19. Summary-ending paragraphs. Test the last sentence of each paragraph of two or more sentences. Target 0.

```
^(?:In short|In summary|To summarize|To sum up|Overall|In other words|Put simply|Simply put|Taken together|Together, these|All told|In essence|Ultimately|The upshot|The bottom line|This means|This is why|That is why|Which is why|The result is|The lesson is|The takeaway is)\b
```

C20. Demonstrative and aphoristic closers. Test the last sentence of each paragraph. At most 1 per chapter.

```
^(?:This|That|These|Those|Such)\s+(?:is|are|was|means|makes|shows|ensures|gives|matters|explains|keeps|lets|turns|leaves|marks|reflects)\b
```

C21. Signposting and self-reference. Outside the Chapter 1 roadmap, target 0 for the first pattern; "this chapter", "this section" and "this document" at most 2 per chapter.

```
(?i)\b(?:this|the (?:next|following|previous|present|rest of the)|later|subsequent)\s+(?:chapter|section|subsection|part|document)s?\s+(?:will\s+)?(?:explores?|examines?|discuss(?:es)?|describes?|turns? to|looks? at|presents?|introduces?|covers?|addresses?|delves?)\b|\b(?:as we will see|we will|let us|let's|we now turn|now we turn|we begin by|before we|in what follows|as (?:discussed|mentioned|noted|shown) (?:above|below|earlier|previously))\b
self: (?i)\bthis (?:chapter|section|document)\b
```

C22. Rhetorical questions and colon reveals. Target 0. Exempt numbered lists of open questions and the MPS "Open Questions" section.

```
question: (?m)^(?!#|\||\s*\d+\.|\s*[-*+] ).*\w\?(?=\s|$)
reveal:   (?:^|(?<=[.!?] ))(?:The|One|Here is the)\s+(?:result|answer|catch|point|key|lesson|takeaway|upshot|twist|problem|kicker|bottom line|short version|good news|bad news)(?:\s+is)?:\s
```

C23. Bullets-to-prose ratio. Count list items and prose paragraphs per chapter. Flag a ratio above 0.35 in Chapters 1 to 12 (the GossipSub v1.1 specification measures 0.32; the current draft 0.21). Flag any list of fewer than three items, any list item over 40 words, and any list item that starts with "So", "Therefore", "Because" or "This".

```
item: (?m)^\s*(?:[-*+]|\d+\.)\s
```

C24. Bold and emphasis. Bold run-in list items target 0. Bold outside Appendix A identifiers, figure captions and a glossary term's defining use is flagged; italics used for emphasis rather than titles or EARS keywords are flagged.

```
run-in: (?m)^\s*(?:[-*+]|\d+\.)\s+\*\*[^*]+\*\*\s*[:.\u2014-]
bold:   \*\*(?!MPE-|Figure|Table)[^*\n]+\*\*
```

C25. Heading case. Flag any heading with two or more capitalized words after the first, then clear those that are proper nouns, glossary terms or fixed template headings (Section 2).

```
(?m)^#{1,6}\s+[A-Z][\w-]*(?:\s+(?:of|and|the|a|an|in|on|for|to|or|with|by|at)?\s*[A-Z][a-z][\w-]*){2,}\s*(?:\{[^}]*\})?\s*$
```

C26. Banned heading forms. Target 0 outside Chapter 1's "Introduction", Chapter 12's "Conclusion" and the fixed MIP and MPS headings.

```
announce: (?m)^#{1,6}\s+(?:Understanding|Exploring|Navigating|Unpacking|Demystifying|Diving|Delving|Unlocking|Harnessing|Leveraging|Embracing|Mastering|Introducing|Examining|Unveiling|Decoding|Rethinking|Reimagining|Revisiting|Towards?|Beyond|A Closer Look|A Deep Dive)\b
role-of:  (?im)^#{1,6}\s+(?:The\s+)?(?:Role|Importance|Power|Significance|Future|Art|Anatomy|Landscape|Rise|Promise|Journey|Evolution|Impact)\s+(?:of|for)\b
stock:    (?im)^#{1,6}\s+(?:Key\s+(?:Takeaways?|Insights?|Considerations?|Features?|Benefits?|Concepts?|Findings?|Points?)|Final\s+Thoughts|Concluding\s+Remarks|Wrapping\s+Up|Looking\s+Ahead|Next\s+Steps|The\s+Road\s+Ahead|The\s+Bottom\s+Line|Why\s+(?:It|This)\s+Matters|Putting\s+It\s+All\s+Together|How\s+It\s+Works|Challenges\s+and\s+\w+|Future\s+(?:Directions|Outlook|Prospects|Work)|Overview|Summary|Background|Discussion|Considerations|Miscellaneous|Other)\s*(?:\{[^}]*\})?\s*$
```

C27. Heading shape. Flag questions, colons (except "Option N:", "Part", "Appendix" and the problem statement's title), ending full stops, gerund first words (except the fixed "Testing" and "Versioning"), headings over eight words, two headings with no text between them, a section under 120 words, and a section with exactly one subsection.

```
question: (?m)^#{1,6}\s+.*\?\s*(?:\{[^}]*\})?\s*$
colon:    (?m)^#{1,6}\s+(?!Option \d|Part [IVX]+|Appendix [A-Z]|Midnight Problem Statement)[^:{\n]+:\s+\S
period:   (?m)^#{1,6}\s+.*[^.]\.\s*(?:\{[^}]*\})?\s*$
gerund:   (?m)^#{2,6}\s+(?!Testing\b|Versioning\b)[A-Z][a-z]+ing\b
long:     (?m)^#{1,6}\s+(?:\S+\s+){8,}\S+
stacked:  (?m)^#{1,6} [^\n]*\n(?:[ \t]*\n)*#{1,6} 
```

C28. First sentence after a heading. Target 0 for a first word that leans on the heading; flag a first sentence that shares 60 percent or more of the heading's content words.

```
(?m)^#{1,6} [^\n]*\n\s*\n(?:This|These|That|It|They|Such|Here)\b
```

C29. Glossary variants. Each match is checked against STYLE.md's vocabulary; most are errors.

```
\bMPE\b(?!-)|\bthe (?:private event )?bus\b|\bPhase [0-2]\b|(?<!admission )(?<!consumption )\bnullifiers?\b|\bepochs?\b|\bfallback\b|\bbridge\b|(?<!GossipSub )\btopics?\b|(?<!Recognition )\bTags?\b|(?<!Bus )\bRegistry\b|(?<!Bus )\bOperators?\b|(?<!Bus )(?<!Store )(?<!Midnight )\bnodes?\b
```

C30. Provenance leaks and typographic residue. Target 0, including in Appendix A. "Audit" is allowed only when citing a third-party security audit by key.

```
leaks:  (?i)\b(LLM|GPT|Claude|Opus|Sonnet|Grok|Codex|Luna|prompt(?:s|ed)?|drafts?|revision|earlier version|reviewers?|panel|persona|council|scraped|fetched|unverified|predicted|formerly|renamed|alignment study)\b|\b[gw]\d\b
curly:  [\u201C\u201D\u2018\u2019]
emoji:  [\U0001F300-\U0001FAFF\u2600-\u27BF]
rules:  (?m)^(?:-{3,}|\*{3,}|_{3,})\s*$
```

## 5. Sources

Primary catalogues and tools

- Wikipedia, "Signs of AI writing" (WikiProject AI Cleanup): https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing. The pattern families and word lists by model era, copula avoidance with the reported 10 percent fall in "is" and "are", the three forms of negative parallelism, title case and heading tells, section summaries, unusual tables, the caveats on detectors and human judgement, the list of ineffective indicators, and the human-syntax features (plain verbs, simple is/has, hedges such as "perhaps" and "tends to").
- blader/humanizer, README: https://github.com/blader/humanizer. The current 26-pattern grouping (staging instead of stating, rhythm by rule, inflation, formatting by rule, chat leftovers, writing for the wrong reader) and its five strongest tells.
- Humanizer skill 2.9.1, local copy at ~/.claude/skills/humanizer/SKILL.md. The 33-pattern version with before and after examples, the false-positive list, and the rule never to invent facts in a rewrite.

Studies of model prose

- Kobak, González-Márquez, Horvát and Lause, "Delving into LLM-assisted writing in biomedical publications through excess vocabulary", Science Advances 11(27), 2025: https://arxiv.org/abs/2406.07016. Lower bound of 13.5 percent LLM-processed 2024 PubMed abstracts; frequency ratios for "delves", "underscores", "showcasing"; excess style words mostly verbs.
- Juzek and Ward, "Why Does ChatGPT 'Delve' So Much?": https://arxiv.org/abs/2412.11385. The 21 focal words with their 2020 to 2024 increases, and evidence consistent with preference tuning as a cause.
- Liang and colleagues, "Monitoring AI-Modified Content at Scale": https://arxiv.org/abs/2403.07183. Between 6.5 and 16.9 percent of AI-conference peer-review text substantially model-modified; the 9.8, 34.7 and 11.2-fold rises of "commendable", "meticulous" and "intricate"; top adjective and adverb lists.
- Liang and colleagues, "Mapping the Increasing Use of LLMs in Scientific Papers": https://arxiv.org/abs/2404.01268. Up to 17.5 percent model-modified computer science papers, against 6.3 percent in mathematics.
- Geng and Trotta, "Is ChatGPT Transforming Academics' Writing Style?": https://arxiv.org/abs/2404.08627. About 35 percent of computer science arXiv abstracts carry the style of a simple "revise the following sentences" prompt.
- Reinhart and colleagues, "Do LLMs write like humans? Variation in grammatical and rhetorical styles", PNAS 122 (2025): https://arxiv.org/abs/2410.16107. Participial clauses at 2 to 5 times the human rate, nominalizations at 1.5 to 2 times, half the human rate of agentless passives.
- Russell, Karpinska and Iyyer, "People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text": https://arxiv.org/abs/2501.15654. Expert detection rates, robustness to humanization, and the frequency of each clue category.
- Sun, Yin, Xu, Kolter and Liu, "Idiosyncrasies in Large Language Models": https://arxiv.org/abs/2502.12150. Five-way model identification at 97.1 percent that survives rewriting, so the signal lies partly in content.
- Shaib, Chakrabarty, Garcia-Olano and Wallace, "Measuring AI 'Slop' in Text": https://arxiv.org/abs/2509.19163. Expert taxonomy of slop (density, relevance, factuality, bias, repetition, templatedness, coherence, fluency, verbosity, word complexity, tone); verbosity as the agreed indicator.
- Oh, Lee, Ahn, Kim and Kang, "Science or Slop?": https://arxiv.org/abs/2610.00531. Six structural measures for long technical documents (cross-section references, macro redundancy, argument graph, citation isolation, figure exposition, evidence gap), their link to lower review scores, and the overcorrection of metric-driven revision.
- Czuma, "Em-ergence of the em-dash": https://arxiv.org/abs/2606.29540. Pre-registered measurement: medRxiv Discussion sections with an em dash rose from 4.23 to 11.58 percent after ChatGPT, reaching 20.3 percent in 2025; a population indicator, not a per-paper detector.

Style guides and specifications

- Google developer documentation style guide, Headings: https://developers.google.com/style/headings. Sentence case, noun phrases for conceptual headings, no "-ing" first word, no empty or stacked headings, no skipped levels, no links.
- Google developer documentation style guide, Dashes: https://developers.google.com/style/dashes. Colons or full stops rather than dashes between an item and its description.
- Google developer documentation style guide, Voice and tone: https://developers.google.com/style/tone. Against "simply", "it's easy" and identical sentence openings; read the text aloud.
- Google developer documentation style guide, Word list: https://developers.google.com/style/word-list. "Leverage" only when no precise verb exists; "utilize" not for "use".
- Google Technical Writing One, Paragraphs: https://developers.google.com/tech-writing/one/paragraphs. Opening sentences carry the paragraph; one topic per paragraph; delete sentences about past or future topics.
- Google Technical Writing One, Lists and tables: https://developers.google.com/tech-writing/one/lists-and-tables. Parallel lists, an introductory sentence before every list and table.
- Microsoft Writing Style Guide, Headings: https://learn.microsoft.com/en-us/style-guide/scannable-content/headings. Sentence case, parallel structure per level, no single subheading, no two headings without text, short and specific headings, run-in headings for repeated item types.
- Microsoft Writing Style Guide, Use simple words, concise sentences: https://learn.microsoft.com/en-us/style-guide/word-choice/use-simple-words-concise-sentences. One term per concept; cut words that add no substance.
- Wikipedia, Manual of Style, Section headings: https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style#Section_headings. Sentence case, no reference back to the parent subject, no question headings, unique headings.
- RFC 7322, RFC Style Guide: https://www.rfc-editor.org/rfc/rfc7322. Title-case section titles as house style, the self-contained Abstract, expansion of abbreviations at first use, consistent terms across documents.
- RFC 3552, Guidelines for Writing RFC Text on Security Considerations: https://www.rfc-editor.org/rfc/rfc3552. A Security Considerations section states which attacks are out of scope and why, which are in scope, and the assumptions authentication rests on.
- RFC 8174, Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words: https://www.rfc-editor.org/rfc/rfc8174. Only uppercase MUST, SHOULD and MAY carry normative meaning.
- PEP 12, Sample reStructuredText PEP Template: https://peps.python.org/pep-0012/. Fixed section names and book-title case as a template convention.
- Rust RFC template: https://github.com/rust-lang/rfcs/blob/master/0000-template.md. Fixed section names (Summary, Motivation, Guide-level and Reference-level explanation, Drawbacks, Rationale and alternatives, Prior art, Unresolved questions, Future possibilities).
- libp2p, gossipsub v1.1 specification: https://github.com/libp2p/specs/blob/master/pubsub/gossipsub/gossipsub-v1.1.md. A human-written protocol text in this document's domain: noun-phrase headings naming mechanisms and parameters, and the sentence and paragraph variance figures used as calibration in Sections 3 and 4.
- Midnight Foundation, MIP template, MPS template, MIP-0002, MIP-0013 and MIP-0019: https://github.com/midnightntwrk/midnight-improvement-proposals (local copy in ~/midnight/midnight-improvement-proposals). The fixed proposal and problem-statement headings, the template's statement that its headings are part of the structure, and the Foundation's own heading and paragraph habits.

Writing craft

- Knuth, Larrabee and Roberts, Mathematical Writing (Stanford CS-TR-89-1193): https://jmlr.csail.mit.edu/reviewing-papers/knuth_mathematical_writing.pdf. Text must read correctly with subheadings removed; one notation per thing; rhythm checked by ear; no superlatives about one's own work.
- Lamport, "State the Problem Before Describing the Solution": https://lamport.azurewebsites.net/pubs/state-the-problem.pdf. Correctness conditions come before the solution, in terms independent of it.
- Gopen and Swan, "The Science of Scientific Writing", American Scientist 1990: https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf. Topic and stress positions; put the action in the verb; context before new information.
- Orwell, "Politics and the English Language": https://www.orwellfoundation.com/the-orwell-foundation/orwell/essays-and-other-works/politics-and-the-english-language/. The six rules against stale figures, long words, removable words, needless passives and jargon.
- Slab, "The Writing Culture at Stripe": https://slab.com/blog/stripe-writing-culture/. Narrative documents over slides, and footnotes that move peripheral material out of the main line.
