# Bitmessage: A Comprehensive Technical Guide to Its Protocol, Privacy, Security, Implementations, and Future

**Research date:** October 1, 2026  
**Primary implementation examined:** PyBitmessage default branch `v0.6`, pinned where relevant to commit `dcbcc4a2fd74a9c7119fa48c5a54457a6ef8887a`, committed May 29, 2026. fileciteturn19file0L2-L2

**Contents:** Executive assessment and history; architecture and protocol; cryptography and delivery; privacy and security; proof of work, scalability, and implementation status; comparison and modernization; verification, reference material, and final assessment.

## Executive assessment, history, and current status

Bitmessage is an asynchronous peer-to-peer messaging protocol proposed by Jonathan Warren in a paper dated November 27, 2012. Its central idea was unusual for secure messaging: rather than merely encrypting message contents while sending them through identifiable mailboxes, Bitmessage attempted to obscure *which encrypted object belongs to whom* by disseminating objects through a peer-to-peer network. An ordinary relay is therefore supposed to see encrypted objects without being told which user is the recipient. The original paper explicitly framed the problem as hiding both content and “non-content” information such as sender and receiver identities. citeturn22view0

Bitmessage borrowed aspects of Bitcoin's peer-to-peer dissemination model and Hashcash-like proof-of-work, but it is **not a blockchain system**. The protocol has no blockchain, block production, longest-chain or other consensus rule, native currency, mining subsidy, account balance, transaction fee, or ledger whose global state must be agreed upon. Its standard propagating objects are `getpubkey`, `pubkey`, `msg`, and `broadcast`; proof-of-work is attached to individual objects as an admission and anti-spam cost. The original paper said its transfer mechanism was *similar* to Bitcoin transaction/block propagation, not that Bitmessage itself maintained a blockchain. citeturn22view0turn22view1turn22view3

The architecture is therefore best understood as:

> **encrypted publish-and-replicate messaging + cryptographic addresses + per-object proof-of-work + recipient-side recognition**

rather than “email on a blockchain.”

The original whitepaper's famous simplification was that “all users would receive all messages” and individually try their private keys. That captures the privacy idea but not every protocol detail. Bitmessage divides the address space into **streams**, and objects propagate in the relevant stream; peer-to-peer maintenance messages such as `version`, `addr`, `inv`, and `getdata` are not themselves application objects disseminated indefinitely. The paper's hierarchical stream scheme was presented as a proposed scalability mechanism rather than proof that a mature multi-stream network had already been deployed. citeturn22view0turn22view1

The protocol evolved materially after the 2012 paper. Current documentation identifies protocol version 3 as the network object protocol expected since November 16, 2014, while address versions separately evolved through versions 1–4. Address version 4 was specifically designed to reduce passive harvesting of users' public keys: a public-key request uses an address-derived tag, and the returned public-key material is encrypted so that possession of the full Bitmessage address is needed to recover it. citeturn22view1turn22view4

This distinction between version namespaces matters:

| Namespace | What it versions | Examples |
|---|---|---|
| Protocol version | Peer/network behavior | Protocol v3 |
| Address version | Address/public-key construction | v2, v3, v4 |
| Object version | Format of a particular propagating object | Varies by object |
| Client release | Software package | PyBitmessage 0.6.2, 0.6.3.2 |

Conflating these leads to errors such as assuming that “Bitmessage v4” means a fourth network protocol.

**The strongest defensible property** is content confidentiality against relays that do not possess the recipient's decryption key, subject to the security of the cryptographic implementation and endpoints. A message also carries a signature associated with the sender's Bitmessage identity, providing cryptographic authentication of control of that address's signing key. This does **not** establish that a Bitmessage address belongs to a particular real-world person: that association still has to be learned through a trusted channel or other authentication mechanism. citeturn22view1turn22view2

The strongest claim that should *not* be made is that Bitmessage makes communication “untraceable.” Flooding removes the obvious server-side recipient mailbox from the baseline design, but timing, peer topology, packet volume, online/offline behavior, public-key requests, acknowledgements, Sybil participation, eclipse attacks, and large-scale traffic correlation remain relevant. Warren's own paper acknowledged that an observer who sees an acknowledgement originate first at a particular machine could infer that the recipient is there. citeturn22view0

A second important limitation is cryptographic: baseline Bitmessage does **not provide modern per-message forward secrecy**. Its encrypted payload contains a fresh ephemeral public key, but encryption is ultimately derived from an ECDH computation involving that ephemeral key and the recipient's long-term address encryption key. An adversary that records old ciphertext and later obtains the recipient's long-term private encryption key can reconstruct the old ECDH shared secrets from the archived ephemeral public keys. This follows directly from the encryption construction; the protocol documentation itself treats forward secrecy as a later/proposed capability rather than a property of the deployed baseline. citeturn22view1turn22view2

The software picture in 2026 is mixed. The official GitHub repository is not archived; its default branch remains `v0.6`, and there were substantive commits through May 29, 2026. The pinned head examined here is `dcbcc4a2...`, signed by maintainer Peter Surda. fileciteturn1file0L2-L2 fileciteturn19file0L2-L2

But the **release train is dramatically older than the source tree**. The most recent public GitHub emergency-release sequence remains 0.6.3/0.6.3.2 from February 2018. Release 0.6.3 was published to fix a remote-code-execution vulnerability in 0.6.2; 0.6.3.2 followed with stricter mitigation. fileciteturn11file0L2-L2

The branch also retains striking technical debt. Its `setup.py` still begins with a Python 2.7 shebang and advertises a “Python :: 2.7 :: Only” classifier, even while other parts of the tree contain Python 3 and alternative-UI work. The correct description is therefore **active source maintenance atop a stale and transitional release/dependency base**, not simply “dead software” and not a modern, routinely released secure-messaging stack. fileciteturn8file0L2-L2

The project wiki itself says that an independent security audit is needed. This research located historical analyses, the 2018 vulnerability record, source-level security changes, and general secure-messaging research, but **did not locate a recent, comprehensive independent audit of the current 2026 PyBitmessage tree**. Absence of such an audit in this search is not proof that no review has ever occurred. citeturn22view5

Accordingly, the practical assessment is differentiated:

| Use | Assessment |
|---|---|
| Protocol/history education | **Good research subject.** It illustrates flooding-based metadata protection, proof-of-work admission, self-authenticating addresses, and privacy/scalability tradeoffs. |
| Controlled experimentation | **Reasonable with isolation.** Use test identities, pinned source, a VM/container, and non-sensitive traffic. |
| New application integration | **High engineering burden.** Protocol and implementation age, dependency issues, key-management model, and release status require substantial review. |
| Routine personal messaging | **Technically possible, but alternatives have substantially more modern session security and usability.** |
| High-risk anonymity | **Not defensible on current evidence.** No strong global-observer anonymity guarantee, no baseline forward secrecy, limited recent assurance, and endpoint/client age dominate the risk assessment. |

There is also an evidence boundary worth stating explicitly: this research verified current repository activity and protocol/source behavior, but did **not** perform a live census of the public Bitmessage network. No defensible current user count, message rate, anonymity-set size, or active-node population should be inferred from repository activity.

## Architecture, identities, and protocol mechanics

Bitmessage's architecture makes more sense when separated into three layers:

1. **Peer transport:** nodes discover and connect to other Bitmessage nodes.
2. **Object dissemination:** inventory identifiers announce propagating objects; peers fetch objects they lack.
3. **Recipient processing:** every relevant recipient tests whether an object is meaningful/decryptable for one of its identities.

The protocol specification distinguishes `version`, `verack`, `addr`, `inv`, `getdata`, and `object`. It states that the propagating application container is the `object` message; object types include public-key requests, public keys, private messages, and broadcasts. Inventory identifiers are the first 32 bytes of a double-SHA-512 hash of an object. citeturn22view1

**Architecture**

```text
                     Initial peer discovery
                  bootstrap / learned peers
                           |
                           v
                  +------------------+
                  |  Bitmessage P2P  |
                  |     overlay      |
                  +------------------+
                    /       |       \
                   /        |        \
                  v         v         v

        +-----------+   +-------+   +-------+   +-----------+
        | Alice     |<->| Relay |<->| Relay |<->| Bob       |
        | node      |   |   A   |   |   B   |   | node      |
        +-----------+   +-------+   +-------+   +-----------+
          |                                           |
      private keys                                private keys
      local DB                                    local DB

           inventory announcement: hash(object)
                           |
                     peer requests object
                           |
           +----------------------------------+
           | nonce / expiry / type / stream  |  public
           |----------------------------------|
           | encrypted recipient payload     |  opaque to relays
           +----------------------------------+

       Optional Dandelion-style stem forwarding before wider diffusion
```

This representation reflects the protocol specification and the current PyBitmessage networking implementation; it should not be interpreted as a claim that every reachable node has identical topology or that every deployed node enables the same optional mechanisms. citeturn22view1 fileciteturn13file0L2-L4

**Peer establishment.** The wire protocol uses a 24-byte outer message header:

| Field | Size | Meaning |
|---|---:|---|
| `magic` | 4 bytes | Network marker; mainnet is `0xE9BEB4D9` |
| `command` | 12 bytes | Null-padded command |
| `length` | 4 bytes | Payload length |
| `checksum` | 4 bytes | First four bytes of SHA-512(payload) |
| payload | variable | Command data |

Integers are big-endian, unlike Bitcoin's usual wire convention. Variable-length integers must use their shortest canonical encoding; a longer representation of the same value is malformed. citeturn22view1

Current PyBitmessage source agrees on the mainnet magic value and defines protocol version 3. It sets `MAX_ADDR_COUNT=1000`, `MAX_OBJECT_COUNT=50000`, `MAX_OBJECT_PAYLOAD_SIZE=2**18`, and a one-hour maximum time offset. Its general `MAX_MESSAGE_SIZE` is 1,600,100 bytes, whereas the wiki protocol text says there is no reason for a framed payload to exceed 1,600,003 bytes. That small difference is a useful example of why an implementation review must not simply assume wiki constants and code constants are identical. citeturn22view1 fileciteturn5file0L2-L2

After a `version`/`verack` exchange, peers advertise addresses and inventories. `inv` gives object hashes; `getdata` asks for objects; `object` carries the actual propagating data. Standard object types are:

| Type | Value | Purpose |
|---|---:|---|
| `getpubkey` | 0 | Request an address's public-key material |
| `pubkey` | 1 | Publish public-key material |
| `msg` | 2 | Private message |
| `broadcast` | 3 | Subscriber-readable publication |

The current PyBitmessage tree additionally defines implementation-level object constants related to onion/I2P/address behavior. These should be treated as implementation extensions unless separately standardized; the main public protocol table still centers on the four types above. citeturn22view1 fileciteturn5file0L2-L2

A Bitmessage address is not the public key itself. Modern identities use two elliptic-curve key pairs: one for signing and one for encryption. Current code computes the address hash as:

\[
RIPE = RIPEMD160(SHA512(K_{sign} \,\|\, K_{enc}))
\]

and encodes version, stream, a possibly shortened RIPE representation, and a four-byte double-SHA-512 checksum using Bitcoin-style Base58, prefixed by `BM-`. Current address code supports address versions through version 4 and enforces canonical variable-length integers and version-4 non-malleable leading-zero handling. citeturn22view4 fileciteturn4file0L2-L2 fileciteturn9file0L2-L2

A worked example from the project's address documentation is:

```text
BM-BcbRqcFFSQUUmXFKsPJgVQPSiFA3Xash
```

Independent decoding using the current algorithm yields the byte sequence:

```text
02 01 df2482c42dc5b0797121b9447b1d99bdc3d4 ca229190
^^ ^^ \----------------------------------/ \------/
v2 s1          embedded RIPE                checksum
```

The checksum `ca229190` equals the first four bytes of double-SHA-512 over the preceding data. For address version 2, the 18-byte embedded RIPE value is expanded with two leading zero bytes during decoding. Corrupting even one Base58 character will, with overwhelming probability, cause the checksum test to fail. The source address and encoding rules are documented by the project; the byte decomposition above is a reproduced calculation performed for this report. citeturn22view4 fileciteturn9file0L2-L2

Address versions reflect important historical changes. The project documentation describes version 1 as an obsolete RSA-era format; version 2 moved to separate elliptic-curve signing and encryption keys; version 3 added recipient-selectable proof-of-work parameters and signed public keys; and version 4 added protection against passive address/public-key harvesting. citeturn22view4

**First contact is more elaborate than later contact.** Suppose Alice knows Bob's version-4 Bitmessage address but does not yet have his public key:

```text
Alice                                              Bob / network
  |                                                     |
  | derive address tag                                  |
  | create getpubkey object + PoW                       |
  |---------------------------------------------------->|
  |        object propagates through Bob's stream       |
  |                                                     |
  |                           Bob recognizes his tag    |
  |                           builds v4 pubkey object   |
  |<----------------------------------------------------|
  |         encrypted pubkey object + tag + PoW         |
  |                                                     |
  | derive key from Bob's address; decrypt pubkey       |
  | verify address binding; cache pubkey                 |
  |                                                     |
  | construct signed inner message                      |
  | encrypt to Bob's long-term encryption key           |
  | perform PoW                                          |
  |------------------ msg object ----------------------->|
  |             stem / flood / inventory relay          |
  |                                                     |
  |                          Bob decrypts and verifies  |
  |                          destination and signature  |
  |                                                     |
  |<--------------- embedded ACK relayed ---------------|
```

For subsequent messages, Alice can normally use Bob's cached public key and skip the public-key-discovery exchange. Version-4 tags are important because a node observing a `getpubkey` request should not be handed the recipient's complete RIPE hash, while the requester—who knows the full address—can still recognize and decrypt the public-key response. citeturn22view1turn22view4

That does **not** make an address secret by itself. A publicly posted Bitmessage address can be copied by anyone, and anyone knowing it has whatever capabilities the protocol intentionally gives address holders—for example, obtaining the associated public-key information needed to communicate with that address. Address secrecy and private-key secrecy are different properties.

Random and deterministic identities are both supported in the project design. Current code generates random 32-byte private keys from the operating system's random source and can derive deterministic private material using SHA-512 over a passphrase-plus-nonce construction. The wiki consequently warns that deterministic identities rely heavily on passphrase strength. A low-entropy human phrase is not magically strengthened into a secure identity merely because its output is 256 bits long. citeturn22view4 fileciteturn4file0L2-L2

Bitmessage's current source still boots into stream 1. The original whitepaper described a binary hierarchy of parent and child streams as the eventual scaling mechanism: users in different streams could temporarily navigate through parent/child peer sets to reach a destination stream. That was a *design proposal*. It should not be cited as proof that a large, automatically balanced hierarchy exists on today's public network. citeturn22view0

Current peer discovery also creates practical infrastructure dependencies. The current connection-pool code knows project bootstrap hostnames using ports 8080 or 8444 and has SOCKS/onion-specific bootstrap behavior. Once bootstrapped, nodes learn addresses from peers. Current connection selection also tries to avoid multiple outbound peers from the same network group as a defense against adversarial concentration. These mechanisms reduce—but do not eliminate—the significance of the bootstrap infrastructure or the risk of peer-manipulation attacks. fileciteturn17file0L2-L4

## Cryptography, delivery, and communication modes

Bitmessage's message encryption is an ECIES-like hybrid construction built around the `secp256k1` elliptic curve. Current PyBitmessage code explicitly instantiates `secp256k1` for key multiplication and encryption operations. The encrypted-payload format contains a 16-byte IV, an ephemeral elliptic-curve public point \(R\), ciphertext, and a 32-byte HMAC-SHA-256. citeturn22view1turn22view2 fileciteturn4file0L2-L2

In simplified notation, Bob's long-term encryption key pair is:

\[
k,\quad K=kG
\]

Alice creates a fresh ephemeral key:

\[
r,\quad R=rG
\]

and both sides can derive:

\[
P=rK=kR
\]

The protocol hashes the shared point material with SHA-512 and splits the result into encryption and MAC key material. The documented encryption mode is AES-256-CBC with PKCS#7 padding, while integrity is provided separately with HMAC-SHA-256 over the IV, ephemeral public-key encoding and ciphertext. citeturn22view2turn22view1

Conceptually:

```text
recipient long-term public key K
              |
random r ---> ECDH(r, K) ---> SHA-512
                 |             /     \
                 |         AES key   MAC key
                 |             |        |
random IV ----------------> AES-CBC     |
plaintext -----------------> encrypt     |
                              |          |
                           ciphertext ---+--> HMAC-SHA256
```

The important distinction is that **ephemeral sender-side ECDH is not equivalent to forward secrecy**. An archive contains \(R\). If Bob's long-term \(k\) is compromised later, an attacker computes \(kR\) for each recorded message and derives the old symmetric keys. Modern forward-secret messengers instead evolve or destroy session key material so that loss of a current identity/session state does not automatically recover every old message. The Bitmessage protocol's own feature list has treated forward secrecy as an extension/proposal, supporting this interpretation. citeturn22view1turn22view2

Bitmessage separately authenticates the sender. The plaintext structure inside a private `msg` object includes the sender's address version and stream, signing and encryption public keys, proof-of-work preference parameters for sufficiently new address versions, the recipient's RIPE hash, message encoding, body, optional acknowledgement data, and an ECDSA signature. The signature covers the object header beginning with the time plus the inner message fields through the acknowledgement data. citeturn22view1

Current PyBitmessage signing code defaults to SHA-256 for signatures but retains verification logic that first accepts historical SHA-1-based signatures and then SHA-256, explicitly as a migration measure. That compatibility behavior is useful for interoperability but is also an example of protocol archaeology accumulating inside a long-lived cryptographic implementation. fileciteturn4file0L2-L2

Authentication is therefore best expressed as:

> “This message was signed by the signing key bound to this Bitmessage address,”

not:

> “The network has proven that Alice Smith wrote this.”

Real-world identity authentication still depends on how the receiver obtained and authenticated Alice's Bitmessage address.

There are also three different encryption domains that should not be confused:

| Domain | What it protects | What it does not protect |
|---|---|---|
| Message-object encryption | Message content from ordinary relays | Source IP, peer timing, endpoint compromise |
| Peer transport protection | An individual network hop | End-to-end identity or global traffic correlation |
| Local device protection | `keys.dat`, message DB, process memory | Network metadata or remote correspondent behavior |

The protocol historically defined a `NODE_SSL` capability for peer transport, and current source retains TLS/SSL-related behavior. But the old wiki language reflects historical TLS assumptions and should not be used as a 2026 recommendation for cryptographic configuration. End-to-end object encryption is the protocol's primary content-security boundary. citeturn22view1 fileciteturn5file0L2-L2

**Acknowledgements.** A message may include pre-built acknowledgement data that the recipient can transmit after successful message processing. The UI documentation describes states such as waiting for acknowledgement and acknowledgement received. Cryptographically, however, this means less than “the human read the message.” At most, an expected acknowledgement indicates that protocol processing associated with the recipient occurred and that the acknowledgement subsequently reached the sender. It does not prove that a person saw the screen, understood the text, retained it, or was the only party controlling the recipient key. citeturn22view1turn22view6

The original whitepaper identified acknowledgements themselves as a privacy problem. If an observer watches a suspected recipient's link and an acknowledgement appears there before elsewhere, the observer gains evidence about the recipient's location. Warren proposed indirect acknowledgement behavior as a mitigation. This is an unusually explicit acknowledgment, in the original design itself, that encrypted flooding is not automatically sufficient to conceal message endpoints. citeturn22view0

**Offline delivery** is also best described as replicated object retention, not a mailbox guarantee. The 2012 paper proposed two-day storage plus repeated sender retransmission with exponential backoff. Protocol v3 later moved to expiry times associated with objects, with documentation allowing substantially longer lifetimes, up to roughly 28 days plus clock allowance. Thus the whitepaper's “two days” is historical design, not a complete statement of current object semantics. citeturn22view0turn22view1

Object expiry only tells compliant nodes when they may stop accepting or retaining an object. It cannot force deletion from:

- a recipient's message database;
- filesystem backups;
- screenshots or exports;
- a malicious relay's archive;
- an adversary's packet capture.

Accordingly, Bitmessage does not provide cryptographic “message deletion” merely because a network object expires.

The protocol's communication modes have meaningfully different properties.

**Private one-to-one messages** use recipient-targeted encryption. The sender's inner identity information and signature become available after successful recipient decryption, so relays do not need the sender address to relay the encrypted object. citeturn22view1turn22view2

**Broadcasts** exploit the same replicated network for publication. Subscribers knowing a broadcaster's Bitmessage address can derive what they need to recognize/decrypt its broadcast objects. A broadcast is therefore authenticated pseudonymous publication, not a private message to an unknowable subscriber set. Someone who knows the broadcast identity is intentionally able to read its broadcasts. citeturn22view0turn22view1

**Subscriptions** are the recipient-side mechanism for following such broadcasters. The whitepaper envisioned them as a way for a pseudonymous authenticated source to publish repeatedly to interested readers. citeturn22view0turn22view7

**Chans**, also described historically as deterministic mailing lists, derive identity material from a shared passphrase. Project help explains that creation and joining are essentially the same deterministic operation. That has a profound security implication: everyone possessing the chan secret can derive the same private keys and can therefore act as the chan identity. A chan provides a shared pseudonymous identity, not cryptographic attribution to individual members, and compromise by one member is effectively compromise of the shared identity. citeturn22view7

For modern group messaging, this is weak membership semantics. Chans have no natural per-member signing identity, fine-grained revocation, sender accountability, or Double-Ratchet-style forward-secret membership evolution merely by virtue of being encrypted. A contemporary group design should instead give members distinguishable credentials and explicit membership-change semantics.

## Privacy threat model, security, and assurance

Bitmessage's most interesting property is not its cipher suite but its attempt to reduce metadata through **receiver-oblivious dissemination**. A relay can forward an encrypted `msg` object without an explicit recipient address in its peer-routing decision. That is fundamentally different from SMTP, where servers route to named domains/mailboxes, and from many centralized messengers, where a service necessarily knows which account queue should receive a particular envelope. citeturn22view0turn22view1

But metadata privacy has several dimensions, and Bitmessage protects them unevenly:

| Property | Baseline assessment |
|---|---|
| Content confidentiality from relays | Strong in design, assuming uncompromised cryptography/endpoints |
| Sender-address confidentiality from relays | Sender identity is inside encrypted message data for private `msg` objects |
| Recipient-address confidentiality from ordinary relays | A primary design strength; relays need not route by recipient identity |
| Source-IP anonymity | Limited; immediate peers see network origin/neighbor information |
| Relationship anonymity | Partial; vulnerable to traffic/timing/topology inference |
| Message unlinkability | Not guaranteed under active/global observation |
| Forward secrecy | Absent from baseline private-message encryption |
| Post-compromise recovery | Absent as a ratcheted messaging property |
| Endpoint security | Outside protocol guarantees |
| Global passive observer resistance | Not established |

These are design/security assessments based on the protocol construction, not claims from a formal proof. citeturn22view0turn22view1turn22view2

A useful adversary matrix is:

| Adversary | What it can observe/do | Principal risk |
|---|---|---|
| Ordinary single relay | Neighbor IP, inventory/object timing and size | First-hop/source inference; traffic fingerprinting |
| User's ISP/local observer | Bitmessage connections, timing, volume, peer IPs unless hidden by overlay | Correlation and classification |
| Malicious correspondent | Knows relationship and plaintext it receives; can time probes | Active confirmation/fingerprinting |
| Many colluding P2P peers | Observe propagation from multiple vantage points | First-spy analysis, topology inference |
| Sybil attacker | Introduces many peers/addresses | Surrounding or biasing a target's peer set |
| Eclipse attacker | Controls most/all target-visible peers | Observation, censorship, withholding, network-view manipulation |
| Global passive observer | Correlates flows over much of the Internet | Strong sender/relationship inference despite encryption |
| Endpoint attacker | Reads keys, messages and memory | Near-total compromise; historical decryption risk |
| Software-supply-chain attacker | Modifies client or release | Complete defeat of cryptographic assurances |

Bitmessage does not inherently stop an immediate peer from knowing “I received this object from IP address X.” Flooding changes the inference from “X definitely sent this message” toward “X may be relaying it,” but the first node seen propagating an object is still statistical information. A sufficiently well-positioned adversary can improve that inference by observing many network locations. Warren's discussion of acknowledgement timing demonstrates that the protocol designers recognized this general class of source-timing problem from the beginning. citeturn22view0

PyBitmessage later added **Dandelion-style propagation**. The 2018 release notes described a Dandelion++ protocol extension intended to improve privacy. In the present source tree, the implementation maintains up to two “stem” connections, reshuffles stem mappings on a 600-second interval and has randomized transition-to-fluff timing. The default configuration currently contains `dandelion = 90`. fileciteturn11file0L2-L2 fileciteturn13file0L2-L4 fileciteturn14file2L25-L33

Conceptually:

```text
traditional flooding:
source -> many peers -> many peers -> network

Dandelion-style:
source -> stem peer -> stem peer -> ... -> "fluff" -> wider network
```

This complicates the simplest “first peer that sent me the object is probably the source” heuristic. It does **not** by itself create the stronger properties of a mix network: there is no general guarantee of layered route anonymity, fixed-rate cover traffic, constant-size messages, large intentional mixing batches, or resistance to an observer that can correlate traffic across many links. That distinction is essential.

Tor can complement Bitmessage by concealing a user's direct IP address from Bitmessage peers, and PyBitmessage supports SOCKS proxy modes and onion-related networking. But the project's help documentation warns that proxying has limitations—particularly around incoming connectivity—and the current code contains separate behavior for SOCKS, onion proxies and bootstrap traffic. A user should therefore verify routing empirically rather than treat “Tor enabled” as a complete anonymity proof. citeturn22view8 fileciteturn17file0L2-L4

Even perfect Tor routing would not solve all Bitmessage privacy questions. Traffic correlation can operate above or below the overlay: an observer can reason about when the user becomes active, when large objects originate, whether ACK-related traffic follows, and how these events coincide elsewhere. Tor changes the network-layer adversary model; it does not transform Bitmessage into a formally analyzed global-observer-resistant messaging system.

**Address version 4 improves public-key-request privacy**, but it does not hide a public address from an adversary who already knows that address. This is a recurring pattern in privacy protocols: a construction may prevent *bulk passive discovery* without providing secrecy against a targeted party possessing the identifier. citeturn22view1turn22view4

**Small anonymity sets are a structural concern.** Flooding achieves useful receiver ambiguity only among plausible participants who receive or relay the same object class. If relatively few nodes are online, if a stream is sparsely populated, or if activity patterns are distinctive, the effective anonymity set may be substantially smaller than the theoretical set of all Bitmessage identities. Because this research did not execute a public-network measurement campaign, the current magnitude of that problem remains **unknown**, rather than safely assumed either large or small.

### Security incident: remote code execution

The most consequential publicly documented PyBitmessage implementation vulnerability is CVE-2018-1000070, associated with PyBitmessage 0.6.2. The project published an emergency 0.6.3 release on February 13, 2018 stating that 0.6.2 contained an exploitable remote-code-execution bug and advising users to upgrade or downgrade. A stricter 0.6.3.2 mitigation followed. The project wiki reported that exploitation had been observed against some users and treated a maintainer's Bitmessage addresses as compromised. fileciteturn11file0L2-L2 citeturn22view5

The fixing commit is unusually informative. Commit `3a8016d31f517775d226aa8b902480f4a3a148a9`, dated February 13, 2018, removed an `eval()` operation used to construct extended message types from message-controlled data and replaced it with module import plus attribute lookup. The patch message was “Fix message encoding bug — prevent loading invalid message types.” fileciteturn10file0L2-L2

This incident teaches a broader lesson: strong end-to-end cryptography does not save an application that feeds decrypted attacker-controlled content to unsafe language features. Protocol crypto, parser safety, application dispatch, UI rendering, dependency integrity, release distribution and endpoint isolation all contribute to actual security.

A concise vulnerability/assurance timeline is:

| Date | Event | Interpretation |
|---|---|---|
| Nov. 27, 2012 | Original Bitmessage paper | Initial design; not current protocol specification |
| Nov. 16, 2014 | Protocol v3 object support expected | Major protocol-generation boundary |
| Mar. 2017 | PyBitmessage 0.6.2 released | Later found RCE-vulnerable |
| Feb. 13, 2018 | Emergency 0.6.3 | Removes exploitable behavior |
| Feb. 13, 2018 onward | 0.6.3.2 stricter mitigation | Recommended remediation for 0.6.2 users |
| 2026 | Default branch still receiving commits | Source maintenance continues despite old tagged releases |

citeturn22view1 fileciteturn11file0L2-L2 fileciteturn19file0L2-L2

The remaining assurance gap is significant. The project's own site has solicited an independent audit, and current source still contains compatibility code around legacy cryptography, historical APIs and runtime generations. What is missing is not necessarily another headline protocol flaw, but a current systematic assurance story: pinned dependency review, modern cryptographic-library migration, parser fuzzing, reproducible release builds, independent code audit, formal protocol analysis and current-network privacy measurement. citeturn22view5 fileciteturn4file0L2-L2

## Proof of work, scalability, implementations, and operations

Bitmessage's proof-of-work is a **resource-admission mechanism**, not consensus. A sender must find a nonce causing a double-SHA-512-derived numeric value to fall below a target. Receiving nodes can check the result cheaply before accepting an object. The network minimums documented for protocol v3 are 1,000 nonce trials per byte and 1,000 extra bytes, with recipients able to demand higher parameters. citeturn22view3turn22view1

Current code calculates a target equivalent to:

\[
T =
\frac{2^{64}}
{N\left[(L+E)+\frac{TTL(L+E)}{2^{16}}\right]}
\]

where \(N\) is `nonceTrialsPerByte`, \(L\) is object length, \(E\) is `payloadLengthExtraBytes`, and `TTL` is remaining lifetime. Recipient-specified parameters below network minima are raised to those minima. For validation, current code also floors extremely short remaining lifetimes to 300 seconds. fileciteturn5file0L2-L2 citeturn22view3

For an illustrative, **not measured**, object with:

\[
L=1000,\quad E=1000,\quad N=1000,\quad TTL=86400\ \text{s},
\]

the denominator becomes:

\[
1000\left(2000+\frac{86400\times2000}{65536}\right)
=4,636,718.75.
\]

Thus:

\[
T \approx 3.9784\times10^{12},
\]

corresponding to a per-trial success probability of approximately:

\[
2.1567\times10^{-7},
\]

or about **4.64 million expected nonce trials**. This arithmetic is derived directly from the current implementation's target formula; it is not a benchmark of any processor. fileciteturn5file0L2-L2

Proof-of-work changes the economics of spam because producing \(n\) accepted objects costs substantially more computation than merely transmitting \(n\) cheap packets. It does **not** create identities, prevent Sybil peers, compensate relays, or establish consensus. Nor is its burden socially neutral: a desktop GPU, a server farm, a compromised botnet and a battery-constrained phone have very different marginal costs. The original whitepaper explicitly treated proof-of-work difficulty as an anti-spam parameter that could be raised if needed. citeturn22view0turn22view3

The protocol also lets a recipient advertise stronger proof-of-work requirements in its public-key information. This is an interesting receiver-controlled anti-abuse mechanism, but it creates a usability tension: the recipient can raise the cost of unsolicited messages only by also raising the cost for legitimate first-time senders. citeturn22view1

### The scalability equation

Let:

- \(\lambda\) = accepted propagating objects per second in a stream;
- \(S\) = mean object size in bytes;
- \(R\) = effective retention duration in seconds;
- \(P\) = number of relaying nodes.

Ignoring protocol overhead, a continuously connected full relay's incoming object volume is approximately:

\[
B_{node} \approx \lambda S.
\]

Steady-state replicated object storage is approximately:

\[
D_{node} \approx \lambda SR.
\]

Network-wide replicated storage becomes approximately:

\[
D_{network} \approx P\lambda SR.
\]

This is the central privacy/scalability tradeoff: copying objects widely makes recipient-specific routing less informative, but means each participating relay pays for traffic unrelated to itself.

Consider purely illustrative 2 KiB objects:

| Traffic assumption | Per-node object ingress | 28-day raw object volume |
|---|---:|---:|
| 10 objects/min | ~28 MiB/day | ~0.77 GiB |
| 100 objects/min | ~281 MiB/day | ~7.69 GiB |
| 1,000 objects/min | ~2.75 GiB/day | ~76.9 GiB |

These figures omit inventory advertisements, TCP/TLS framing, retries, duplicate announcements, database indexes and other overhead. They are scenario calculations, **not measurements of today's Bitmessage network**. The maximum object lifetime and size constraints come from the protocol, while the traffic rates above are invented solely to illustrate scaling. citeturn22view1

This yields an important distinction:

- If the **total traffic rate stays constant** while more users join, per-node flooded data need not increase merely because \(P\) increases, though aggregate system bandwidth does.
- If **each new user contributes messages**, then total \(\lambda\) rises, so every full relay in the same flood domain pays more bandwidth, verification and storage cost.

The original stream hierarchy was intended to address precisely this problem by partitioning replication. But partitioning has a privacy price: a smaller stream can reveal more about who could plausibly be the recipient, and cross-stream communication has its own connectivity patterns. citeturn22view0

Mobile participation is therefore architecturally difficult. A design that improves recipient ambiguity by downloading everybody else's objects competes directly with mobile constraints on battery, radio wakeups, bandwidth and storage. A “light client” can avoid some cost only by outsourcing filtering, retrieval, keys or computation—and each form of outsourcing potentially reintroduces metadata or trust.

### PyBitmessage as an implementation

The official repository describes PyBitmessage as the reference client. Its GitHub metadata showed a public, non-archived Python repository with default branch `v0.6` and source pushes in 2026. The newest examined commit was made May 29, 2026. fileciteturn1file0L2-L2 fileciteturn19file0L2-L2

Some key implementation observations at that commit are:

| Area | Current evidence |
|---|---|
| Network protocol | Version 3; object and packet bounds implemented |
| Cryptography | `secp256k1`, custom/in-tree `pyelliptic`-style OpenSSL bindings, SHA-512 family, ECDSA, legacy SHA-1 verify compatibility |
| Proof of work | CPU plus optional/OpenCL-related machinery present |
| Privacy propagation | Dandelion implementation present |
| Proxying | SOCKS and onion-aware connection classes |
| Storage | SQLite/inventory abstractions |
| Packaging | `setup.py` still explicitly Python 2.7-oriented |
| Releases | Last public GitHub release sequence dates to Feb. 2018 |
| Source maintenance | Active commits through May 2026 |

fileciteturn4file0L2-L2 fileciteturn5file0L2-L2 fileciteturn13file0L2-L4 fileciteturn8file0L2-L2 fileciteturn11file0L2-L2

That combination makes the software awkward to classify. It is neither a frozen historical artifact nor a conventionally maintained contemporary messenger with frequent signed releases. The gap between source-head work and shipped releases is itself a security-management problem: users must decide whether to trust an eight-year-old release artifact or build a newer, less broadly released source revision.

### Safe evaluation workflow

A responsible 2026 evaluation should be treated as security research rather than immediate migration of sensitive communications.

Use an isolated VM or container; create only test identities; do not import an existing high-value deterministic passphrase; pin the exact Git revision under test; inspect dependency versions and build logs; and prevent the local API from being exposed beyond the test machine. These are defensive recommendations based on the software's release age and historical remote-code-execution incident. fileciteturn11file0L2-L2

For the network experiment itself:

1. start with no sensitive local data in the environment;
2. create two test identities;
3. record their address versions and stream numbers;
4. observe initial peer bootstrap;
5. send a first message and distinguish the public-key-discovery phase from the eventual `msg` object;
6. record proof-of-work and status transitions;
7. send a second message and verify that cached public-key behavior avoids first-contact discovery;
8. exercise a broadcast/subscription separately;
9. exercise a chan only to demonstrate shared-key semantics, not as a model of secure private group chat;
10. test proxy/Tor configuration with packet capture so that routing is **observed**, not assumed.

Project help documents SOCKS proxy support and warns that incoming connection behavior needs separate consideration. citeturn22view8

Back up test identity material before experimenting with recovery. The project help distinguishes identity/configuration material from its messages database; protecting the local device is therefore as important as network encryption. Loss or theft of long-term encryption keys has especially serious consequences because of the historical-ciphertext issue described earlier. citeturn22view6turn22view7

Troubleshooting should distinguish failure layers. “Message not acknowledged” might mean public-key discovery has not completed, proof-of-work is still running, no route/peer is available, the recipient is offline, the object expired, the recipient disabled ACK behavior, or the ACK itself did not return. It should never be translated mechanically into “Bob definitely did not read it.”

## Comparative analysis and modernization

The most illuminating comparison is not “which messenger is best?” but **which metadata and state tradeoff each architecture makes**.

| System | Delivery architecture | Metadata/privacy model | Session-security model |
|---|---|---|---|
| Bitmessage | P2P replicated/flooded objects | Conceals explicit recipient routing from ordinary relays | Long-term address keys; no baseline ratcheted FS/PCS |
| OpenPGP email | Mail servers/mailboxes | Email routing metadata remains outside OpenPGP content protection | Object/message encryption and signatures; not an interactive ratchet |
| Signal | Centralized delivery service | Server-mediated delivery; protocol minimizes what service needs to learn | Asynchronous key establishment + Double Ratchet; modern FS/PCS design |
| Matrix | Federated homeservers/rooms | Federated routing and room metadata; E2EE available | Olm/Megolm-family session mechanisms depending on context |
| SimpleX | Pairwise relay queues without global user IDs at protocol level | Designed around per-connection queues and reduced global identity linkage | Ratcheted E2EE; current project documents post-quantum extensions |
| Briar | Direct/Tor and local P2P transports | Avoids central message server; uses Tor for remote peer connectivity | End-to-end secure channels plus offline/local modes |
| Session | Decentralized storage/routing infrastructure | Onion-routed requests and pseudonymous identities | Current protocol evolution has been working toward stronger FS/PQ properties |
| MLS-style group systems | Server-assisted asynchronous group transport | Metadata depends on application transport | Explicit group membership, forward secrecy and post-compromise security |

The Bitmessage characterization is supported by its primary protocol documents. OpenPGP's modern standard, RFC 9580, specifies content encryption, signatures and key formats rather than an anonymous message-routing network. citeturn22view0turn22view1

Signal's modern design demonstrates what Bitmessage's static address cryptography lacks. Signal specifies asynchronous prekey-based establishment for a sender initiating while the recipient may be offline, followed by ratcheting in which message keys evolve over time. Modern Double Ratchet specifications explicitly target forward security and break-in recovery, and newer revisions include post-quantum/hybrid ratchet designs. citeturn18search1turn10search9

Matrix makes a different trade: homeservers and federation provide efficient room delivery and multi-device synchronization rather than flooding every encrypted message to unrelated users. Matrix's current specification family defines federated rooms and end-to-end encryption mechanisms, but its metadata exposure therefore differs structurally from Bitmessage's recipient-oblivious replication. citeturn20search8turn12search4

SimpleX attacks the identifier problem more directly: its official documentation emphasizes pairwise queues and the absence of a network-wide user identifier at the messaging-routing layer, while its current cryptographic documentation describes ratcheted encryption and post-quantum work. This avoids Bitmessage's requirement that privacy be purchased through global or stream-wide object replication. citeturn12search1turn20search4

Briar moves in yet another direction: it avoids dependence on a conventional centralized messaging server, uses Tor for Internet peer connections and also supports local/offline transports. It is especially instructive because metadata protection is achieved through an anonymity transport and peer-to-peer application model rather than “everyone downloads everyone else's messages.” citeturn12search2turn12search6

The lesson is that Bitmessage remains distinctive. Its central privacy primitive is **replication-induced ambiguity**. That is elegant because routing nodes do not need recipient accounts, but expensive because unrelated nodes absorb one another's traffic. Modern systems more often use sophisticated queue identifiers, anonymity routing, private-information-retrieval-like concepts, mix networks, or trusted-but-metadata-minimized delivery services to avoid full flooding.

### A modernization path

Modernization should be divided into compatibility classes; otherwise it is too easy to describe an entirely different protocol and call it “Bitmessage 2.0.”

**Compatible implementation hardening** can happen without changing network objects. The highest-value work would be to complete and formally support a modern Python runtime; eliminate obsolete custom crypto bindings in favor of well-maintained cryptographic libraries; fuzz every externally reachable parser; institute strict memory/CPU budgets before expensive object processing; remove unsafe legacy application-dispatch paths; publish repeatable signed releases; automate dependency/SBOM review; and establish reproducible builds. The RCE history makes parser and application dispatch review particularly important. fileciteturn10file0L2-L2

Legacy SHA-1 verification is a particularly clear modernization target. The current code intentionally verifies both old SHA-1 and newer SHA-256 signatures for compatibility. Removing that path abruptly would break historical interoperability, so the safe solution is a versioned cutoff or object-version rule—not a silent behavior change. fileciteturn4file0L2-L2

**Compatible operational improvements** include stronger bootstrap diversity, better peer-selection resistance to Sybil concentration, explicit proxy leak tests, safer local API defaults, clearer delivery-status wording and configurable resource ceilings. “Acknowledged” should be shown to users as a protocol event, not a human read receipt. Current code already attempts network-group diversity when choosing peers, providing a foundation rather than a complete Sybil defense. fileciteturn17file0L2-L4

**Negotiated protocol extensions** should replace static per-message public-key encryption with asynchronous session establishment followed by a ratchet. A Bitmessage address could remain a long-term authentication identity, while separately published short-lived/prekey material establishes sessions. Once a session exists, message keys should advance and old key material be erased. This would provide a path toward forward secrecy and post-compromise recovery without giving up pseudonymous addresses. Signal's current asynchronous and ratcheting specifications provide a mature reference point for the properties, though Bitmessage would need its own transport- and flooding-aware construction rather than copying Signal byte-for-byte. citeturn18search1turn10search9

The existing encrypt-then-MAC arrangement could also be replaced in a new object version with a contemporary authenticated-encryption construction plus explicit domain separation and transcript binding. The objective is not merely “use a newer cipher”; it is to make object type, protocol version, address/session context and relevant public header data cryptographically unambiguous.

**Chans should not be modernized by simply changing the cipher.** Their weakness is structural: a shared passphrase produces a shared identity. Modern private groups need individual membership credentials, authenticated membership changes, revocation and evolving epoch keys. The IETF's Messaging Layer Security protocol, RFC 9420, is a relevant reference architecture: the MLS working group describes it as asynchronous group key establishment providing forward secrecy and post-compromise security from small groups to groups of thousands. citeturn21search3turn21search25

### Post-quantum migration

Bitmessage's current `secp256k1` ECDH and ECDSA constructions are classical public-key cryptography. A sufficiently capable cryptanalytic quantum computer running Shor's algorithm would threaten both confidentiality-key agreement and signatures. More immediately, the absence of forward secrecy creates a “record now, decrypt later” concern: an attacker can preserve ciphertext today and wait for either conventional key compromise or future cryptanalytic capability.

NIST finalized ML-KEM in FIPS 203 and ML-DSA in FIPS 204 in August 2024 as post-quantum key-encapsulation and signature standards respectively; NIST describes ML-DSA as designed to remain secure against adversaries with a large-scale quantum computer. citeturn21search2

The safest migration pattern for a Bitmessage successor would initially be **hybrid**, not an abrupt replacement:

\[
shared\_secret =
KDF(classical\_secret \,\|\, postquantum\_secret \,\|\, transcript)
\]

so confidentiality remains intact if at least one component survives the relevant attack, subject to a correctly designed combiner. Address authentication can analogously move toward hybrid signatures before classical signatures are eventually retired.

This has costs. Post-quantum public keys, ciphertexts and signatures are larger than current elliptic-curve material, which raises object sizes, bandwidth, storage and proof-of-work costs. Because Bitmessage replicates objects widely, every extra cryptographic byte is multiplied across relays; PQ migration is therefore partly a scalability change, not merely a cryptographic library upgrade.

A PQ initial handshake would also be insufficient on its own. Long-running sessions should refresh secrets so that compromise recovery does not depend forever on one static post-quantum private key. Signal's contemporary ratchet specifications are useful here because they explicitly explore hybrid/post-quantum ratcheting rather than stopping at a post-quantum first-contact handshake. citeturn10search9

Finally, anonymity improvements need to address traffic analysis directly. Useful research directions include size buckets or padding, controlled timing jitter, deliberate mixing, background cover traffic and stronger source-routing privacy. Every one has a measurable cost in latency, bandwidth or battery use. The correct question is not “does padding improve privacy?” but “against which observer, by how much, and at what replicated cost?”

An incompatible successor might therefore decide that global flooding itself should be abandoned. It could combine self-authenticating pseudonymous identities with anonymous relay queues, mixnet delivery or private queue capability identifiers. Such a system would preserve Bitmessage's philosophical focus on metadata while avoiding the requirement that every relay store every relevant encrypted object.

## Verification, reference material, and final assessment

No live adversarial experiments against the public network were executed for this report. The **executed work** consisted of primary-document analysis, examination of the current reference source tree, inspection of relevant commits/releases and reproduction of mathematical/address calculations. The experiments below are therefore **proposed verification procedures**, not reported measurements.

A serious conformance suite should begin with deterministic, local tests:

| Test | Expected property |
|---|---|
| Address decode | Valid address yields exact version, stream and RIPE |
| Corrupt checksum | Decoder rejects it |
| Non-minimal varint | Decoder rejects it |
| Truncated network header | Safe parse failure |
| Oversized packet/object | Rejected before excessive allocation/work |
| Modified ciphertext | HMAC failure |
| Modified IV/ephemeral key | Integrity/decryption failure |
| Modified signed message field | Signature failure |
| PoW just below target | Accepted |
| PoW just above target | Rejected |
| Expired object | Rejected per expiry rules |
| Unknown object type | Behavior matches versioned spec |
| V4 `getpubkey` | Only intended address holder recognizes tag appropriately |
| Cached pubkey | Second send avoids first-contact discovery |
| Disabled ACK | Sender does not misinterpret absence as decryption failure |

These tests follow directly from the protocol's canonical varints, framing, cryptographic payload, proof-of-work and object model. citeturn22view1turn22view2turn22view3

A separate isolated-network experiment should deploy perhaps 20–100 instrumented test nodes under one researcher's control and record timestamps for object creation, stem transmission, inventory announcements, fluff transitions and receipt. By varying the fraction of malicious observer nodes, one could measure the success rate of first-spy source estimation with and without Dandelion. The dependent variable should be source-identification accuracy, not a vague “anonymity score.” Current Dandelion constants can be pinned directly from `dandelion.py`. fileciteturn13file0L2-L4

A Sybil/eclipsing study should likewise be confined to a private network. Manipulate adversarial peer share, subnet distribution and bootstrap information; then measure how often a victim's outbound set becomes attacker-controlled and whether current network-group diversity prevents concentration. This would test the source code's peer-selection defense rather than simply assuming it works. fileciteturn17file0L2-L4

A Tor/proxy experiment should use host-level packet capture. Run the exact pinned client once without a proxy and once with each supported configuration; verify destination IPs, DNS resolution behavior, bootstrap routing, inbound-listener behavior and onion connections. The result should state exactly what escaped outside Tor, if anything. Merely observing “SOCKS5” in the GUI is not evidence of complete routing. Project help and current networking source both show enough configuration complexity to justify this test. citeturn22view8 fileciteturn17file0L2-L4

### Protocol reference

The following is the compact reference for the major current concepts examined in this report:

| Item | Rule |
|---|---|
| Network magic | Mainnet `0xE9BEB4D9` |
| Protocol generation | v3 |
| Endianness | Big-endian |
| Packet header | 4 magic + 12 command + 4 length + 4 checksum |
| Packet checksum | First 4 bytes SHA-512(payload) |
| Inventory ID | First 32 bytes double-SHA-512(object) |
| Standard objects | getpubkey, pubkey, msg, broadcast |
| Standard max object payload | \(2^{18}\) bytes |
| Address digest | RIPEMD-160(SHA-512(signPub \|\| encPub)) |
| Current address generation | Through version 4 |
| Address text | `BM-` + Base58(version \|\| stream \|\| ripe \|\| checksum) |
| ECC | `secp256k1` |
| Payload encryption | ECIES-like ECDH + AES-256-CBC |
| Payload authentication | HMAC-SHA-256 |
| Current signature default | ECDSA with SHA-256; legacy SHA-1 verify compatibility |
| PoW hash | Double SHA-512 |
| Network PoW minima | 1000 trials/byte, 1000 extra bytes |
| Relay privacy extension | Dandelion-style stem/fluff in current PyBitmessage |

citeturn22view1turn22view2turn22view3turn22view4 fileciteturn4file0L2-L2 fileciteturn5file0L2-L2

### Glossary

**Address:** A Base58-encoded, checksummed representation derived from an identity's public keys plus version and stream information. It is a pseudonymous cryptographic identifier, not proof of civil identity. citeturn22view4

**ACK / acknowledgement:** Protocol data sent after successful recipient-side handling of a message; evidence of protocol processing, not proof of human reading. citeturn22view1turn22view6

**Broadcast:** A signed publication intended for subscribers who know the broadcaster's identity rather than one private recipient. citeturn22view0turn22view1

**Chan:** A deterministic/shared Bitmessage identity derived from a shared secret/passphrase; participants share the ability to act as that identity. citeturn22view7

**Dandelion:** Source-obfuscating propagation technique that delays wide flooding by first forwarding an object through a narrower stem path. Current PyBitmessage includes such machinery. fileciteturn13file0L2-L4

**Forward secrecy:** The property that compromise of long-term/current secrets does not reveal prior session messages. Baseline Bitmessage private messaging does not provide this property in the modern ratcheting sense.

**Inventory:** The set/list of object hashes a node knows. Peers announce inventory and request unknown objects. citeturn22view1

**Object:** Propagating Bitmessage data with proof-of-work and lifetime information. Standard object classes are public-key requests, public keys, messages and broadcasts. citeturn22view1

**Post-compromise security:** Ability for a communication session to regain security after an attacker temporarily obtains current key state, once uncompromised key evolution occurs. Baseline Bitmessage does not implement such a ratchet.

**Proof of work:** Cheap-to-check, expensive-to-produce computational condition attached to Bitmessage objects to discourage mass message generation. It is unrelated to blockchain consensus in Bitmessage. citeturn22view3

**RIPE:** In Bitmessage usage, the 20-byte RIPEMD-160 result derived from a SHA-512 hash of public-key material and used in address construction. citeturn22view4

**Stream:** A protocol partition intended to constrain which nodes carry a set of objects, originally proposed as Bitmessage's principal scaling mechanism. citeturn22view0

### Discrepancy register

Several apparent contradictions disappear once source age and status are separated:

| Apparent contradiction | Resolution |
|---|---|
| Whitepaper says objects kept two days; newer protocol allows much longer lifetime | Two-day rule is 2012 design; protocol v3 uses expiry semantics |
| “Everyone gets everything” vs streams | Flooding applies within relevant dissemination domain; streams were introduced/proposed to partition load |
| Current code active in 2026 vs “latest release 2018” | Source branch has new commits; tagged binary/source releases remain old |
| Signature code mentions SHA-1 vs modern SHA-256 | Current signer defaults to SHA-256 while verifier retains SHA-1 compatibility |
| Wiki packet sanity maximum vs code maximum differ slightly | Documentation and implementation constants are not identical; pin implementation when testing |
| Protocol lists four standard objects while code has more constants | Current implementation contains extensions beyond the core public object table |
| Dandelion described as privacy improvement vs Bitmessage “flooding” | Objects may use a stem phase before eventual wider propagation |
| “Encrypted” interpreted as “anonymous” | Content encryption and network-source anonymity are separate properties |

citeturn22view0turn22view1 fileciteturn4file0L2-L2 fileciteturn5file0L2-L2 fileciteturn11file0L2-L2

### Claim-to-evidence summary

| Major conclusion | Status | Evidence |
|---|---|---|
| Bitmessage has no blockchain/coin consensus | **Specified/design inference** | Whitepaper + protocol object model |
| Relays need not know private-message recipient | **Design/specification** | Encrypted `msg` object structure |
| V4 improves pubkey-request privacy | **Specified/implemented** | Address/protocol docs |
| Baseline lacks message forward secrecy | **Cryptographic inference** | Static recipient key + transmitted ephemeral public key |
| ACK does not prove human read | **Protocol inference** | ACK object semantics |
| PyBitmessage contains Dandelion logic | **Implemented** | Current source |
| 0.6.2 had RCE | **Documented incident** | Release record + fixing commit |
| Current source maintained in 2026 | **Observed repository fact** | Signed May 2026 commit |
| Current public network has a particular size | **Unknown** | No live census performed |
| Current tree has undergone comprehensive independent audit | **Unknown / not located** | Project itself asks for audit |

citeturn22view1turn22view2turn22view5 fileciteturn10file0L2-L2 fileciteturn19file0L2-L2

### Annotated bibliography

**Jonathan Warren, “Bitmessage: A Peer-to-Peer Message Authentication and Delivery System,” November 27, 2012.** The foundational design document. Essential for original motivations, flooding, stream hierarchy, broadcasts, offline handling, ACK privacy and spam design. Its weakness as a present-day specification is age: several operational rules were superseded. citeturn22view0

**Bitmessage Protocol Specification.** The most useful normative-style project documentation for protocol v3 framing, object types, canonical varints, cryptographic payload formats, signatures and proof-of-work parameters. It should still be checked against source because some constants and proposed capabilities differ from the current implementation. citeturn22view1

**Bitmessage Encryption documentation.** Primary explanation of the ECIES-like construction: ephemeral elliptic-curve key, ECDH, SHA-512-derived keys, AES-256-CBC and HMAC-SHA-256. It is the crucial source for evaluating historical-ciphertext confidentiality. citeturn22view2

**Bitmessage Proof-of-Work documentation.** Primary description of nonce search, target calculation and protocol-v3 minima. It establishes that proof-of-work is per-object spam/admission control rather than consensus mining. citeturn22view3

**Bitmessage Address documentation.** Historical and current address-version explanation, including deterministic identities and version-4 public-key-harvesting protection. citeturn22view4

**PyBitmessage source tree, default `v0.6` branch.** The strongest source for what current code actually does. Particularly important files include `protocol.py`, `addresses.py`, `highlevelcrypto.py`, networking/Dandelion modules and packaging metadata. The analysis pinned current behavior to commit `dcbcc4a2...`. fileciteturn19file0L2-L2

**PyBitmessage 2018 emergency releases and commit `3a8016d...`.** Primary evidence for the 0.6.2 remote-code-execution incident and its direct `eval()`-removal fix. Especially valuable because the source patch shows the vulnerable programming pattern rather than relying solely on a vulnerability summary. fileciteturn11file0L2-L2 fileciteturn10file0L2-L2

**Unger et al., “SoK: Secure Messaging,” IEEE Symposium on Security and Privacy, 2015.** A broader academic framework for evaluating secure messaging properties, useful for distinguishing transport, trust establishment and conversation-security properties rather than collapsing “encrypted” into “secure.” citeturn21search27

**Signal asynchronous key-agreement and Double Ratchet specifications.** Useful contemporary reference material for the forward secrecy, asynchronous prekey establishment and post-compromise recovery that Bitmessage's static message encryption lacks. citeturn18search1turn10search9

**RFC 9420, Messaging Layer Security.** A modern IETF-standardized reference for authenticated asynchronous group key establishment with forward-secrecy/post-compromise-security goals, directly relevant when considering a successor to chans. citeturn21search3turn21search25

**NIST FIPS 203/204 post-quantum standards.** Relevant to any serious long-term Bitmessage successor because both confidentiality key establishment and signing authentication eventually need migration away from classical elliptic-curve-only assumptions. FIPS 204 standardizes ML-DSA; NIST finalized the first group of PQ standards in 2024. citeturn21search2

### Final assessment

Bitmessage remains one of the more conceptually interesting attempts to build private asynchronous messaging without assigning every communication to a server-visible recipient mailbox. Its key insight is still valuable: **metadata deserves protocol-level protection, not merely payload encryption**. By letting relays disseminate opaque objects without knowing the recipient, Bitmessage asks a fundamentally different question from ordinary encrypted email. citeturn22view0turn22view1

Its second enduring contribution is the unification of pseudonymous identity, encryption and authentication into a compact shareable address. The user does not separately exchange an email address, encryption certificate and signing certificate. That simplicity was central to Warren's original goal and remains attractive. citeturn22view0turn22view4

Its weaknesses are equally architectural. Receiver ambiguity is purchased with replicated bandwidth and storage. Stream partitioning can reduce resource cost only by changing anonymity sets. Source anonymity remains exposed to timing and topology analysis. Proof-of-work prices spam but disproportionately burdens weak devices and does not stop Sybil participation. Static address encryption leaves archived messages vulnerable after recipient-key compromise. Chans share identity keys rather than providing modern group membership security. citeturn22view0turn22view2turn22view3

The software assurance story is the greatest practical obstacle in 2026. It is encouraging that PyBitmessage's reference source still receives signed maintenance commits, but a May 2026 source head coupled with an official tagged release line last updated in February 2018 is not the maintenance model expected for high-risk secure communications. The lingering Python-2-era packaging and compatibility cryptography reinforce that concern. fileciteturn19file0L2-L2 fileciteturn11file0L2-L2 fileciteturn8file0L2-L2

A modern Bitmessage effort should therefore preserve the **ideas**, not freeze the implementation: self-authenticating pseudonymous addresses, recipient-oblivious dissemination, decentralized publication and explicit anti-abuse costs are worth studying. The implementation should be rebuilt around memory-safe or strongly constrained parsing, supported runtimes, maintained cryptographic libraries, reproducible releases, independent audit and rigorous network simulation.

At the protocol level, the priority should be asynchronous forward-secret sessions with post-compromise recovery; explicit modern group membership rather than shared chan identities; hybrid post-quantum key establishment and authentication; cryptographically bound version negotiation to prevent downgrade; and a quantitative metadata-defense model incorporating padding, timing and source propagation rather than relying on flooding alone. Current Signal ratchet research, MLS and standardized post-quantum primitives show that these goals no longer require inventing every cryptographic component from scratch. citeturn10search9turn21search25turn21search2

A more radical successor should question the one feature most closely associated with Bitmessage: full or stream-wide flooding. Anonymous queues, capabilities, mixnets or other privacy-preserving retrieval mechanisms may offer a better scaling curve while retaining the original objective of preventing infrastructure from learning a clean social graph. That is the central open research question: **how much replication is actually necessary to obtain useful recipient ambiguity, and can stronger anonymity be bought more efficiently with mixing and cover traffic?**

Until those questions are answered experimentally and the implementation receives modern independent assurance, Bitmessage is best classified in 2026 as **an historically important, still-maintained experimental privacy protocol with valuable architectural ideas, but not a system for which strong high-risk anonymity or contemporary secure-messaging guarantees can responsibly be asserted**. Its most defensible role today is as a research platform and design case study—and potentially as the foundation for a carefully versioned successor—rather than as an unquestioned replacement for mature modern secure messengers.