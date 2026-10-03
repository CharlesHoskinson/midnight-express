# Post-Bitmessage literature: brief for collection agents

Read `briefs/common.md` first. Its hard rules, tools, working indexes, catalog format and procedure
all apply. This file replaces only the **inclusion test**, the **slice names** and a few catalog
fields.

## What this literature is about

Bitmessage (Warren, 2012) tried to hide who talks to whom by flooding encrypted objects to every
node, attaching proof-of-work to each object, and letting recipients trial-decrypt. The
literature that came after it, or that addresses the same problem better, is the subject of a
review. The review answers four questions:

1. How do later systems hide the **recipient** (receiver privacy) without every node downloading
   everything?
2. How do they hide the **sender and network origin** (source anonymity)?
3. What **session and group security** do they offer (forward secrecy, post-compromise security,
   membership, post-quantum)?
4. What are the proven **limits and costs** (bandwidth, latency, anonymity trade-offs, anti-spam)?

## Inclusion test

Keep a source if it is a primary, citable document (peer-reviewed paper, preprint, thesis, IETF
RFC or draft, protocol specification, whitepaper, security audit, measurement study) that does at
least one of the following:

- designs, analyses, attacks or measures a system for **private or metadata-private messaging,
  publish/subscribe or event delivery**;
- supplies a **building block** that such systems use (mixnet, DC-net, PIR, oblivious or fuzzy
  message retrieval, key-private or stealth addressing, anonymous credentials or rate limiting,
  ratcheting, group key agreement, anonymous propagation, hybrid post-quantum key exchange);
- proves a **limit** or gives a **systematisation** (SoK, survey) on those topics.

Date: 2012 onward. Also keep a short list of **foundational** pre-2012 sources that later papers
rely on (Chaum mixes and DC-nets, Hashcash, Tor, Sphinx, PIR, key-privacy, Mixminion, Off-the-Record).
Tag these `"background": true`. Do not go beyond about 25 background items in the whole wave.

Exclude marketing pages, blog posts without technical content, and sources you cannot identify an
author and date for. Product documentation is acceptable when it is the protocol specification
(for example the SimpleX protocol docs, Session whitepaper, Katzenpost specifications, Nostr NIPs).

## Extra catalog fields

Add to every record:

- `"kind"`: `paper`, `preprint`, `thesis`, `rfc`, `spec`, `whitepaper`, `audit`, `report`.
- `"cluster"`: your slice name.
- `"role"`: one of `system`, `building_block`, `attack_or_audit`, `measurement`, `limit_or_theory`,
  `sok_or_survey`.
- `"background"`: `true` for pre-2012 foundational items, else `false`.
- `"bitmessage_link"`: one line saying how this source relates to Bitmessage's design or its
  weaknesses (recipient ambiguity by flooding, proof-of-work admission, static-key encryption, chans,
  streams, source timing, Dandelion). If there is no link, say "none direct".

Specs and whitepapers that are web pages: save the page text as Markdown with the helper
(`pe_fetch.py text URL`, then write it to `pdfs/SLUG.md` yourself) when no PDF exists, and set
`status` to `downloaded` with the `.md` path. Check the page text is the real document.

## Slice names

Write `catalog/<SLICE>.jsonl` and `notes/<SLICE>.md` with your slice name. Other agents run in
parallel; check `catalog/*.jsonl` for duplicates before each download. A source already
catalogued by a wave-one slice (A to G) is skipped unless it is Bitmessage-relevant and not yet
present under your slice's reading: in that case add a catalog line with `"status":"duplicate"`
and the existing `slug`, nothing else is downloaded.

## Report back

Reply with counts, the ten most important sources, and a list of the open questions the sources
leave. Keep it short.
