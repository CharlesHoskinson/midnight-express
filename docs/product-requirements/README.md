# Product requirements for consideration

This is a **candidate portfolio**, informed by three independent reviews of each competing/traditional design. It does not replace the consolidated protocol requirement register or approve an implementation roadmap.

- [Recommended stack and ranked use cases](recommended-stack-and-use-cases.md): consolidated technology choices, business fit and delivery gates.
- [Top ten use cases](top-ten-use-cases.md): ranked business scenarios, actors, triggers, value hypotheses, acceptance scenarios and dependencies.
- [Machine-readable use-case register](use-cases.json): ten candidate records linked to existing and proposed requirements.
- [Candidate EARS extensions](candidate-ears.md): sixteen product/API obligations with acceptance checks and an open product decision.
- [Machine-readable candidate requirement register](candidate-requirements.json).
- [UmbraDB recovery and future release](umbradb-recovery.md): source/API checks, backend integration boundary and acceptance requirements.
- [Working stack and Semaphore extraction](proposed-stack.md): adopted membership lifecycle, admission boundaries and module interfaces.
- [Semaphore membership option](semaphore-membership-option.md): scoped nullifiers, quota gaps and three-agent findings.
- [Original requirement fit and open-source stack](requirements-fit-and-open-source.md): all twelve areas, remaining components and build sequence.
- [GossipSub + Signal composition option](gossipsub-signal-option.md): three-agent feasibility study and experimental gates.
- [Top ten feature considerations](feature-considerations.md): enabling capabilities kept separate from use cases.
- [Three-agent extraction](../../reviews/competitive-event-systems/extraction.md) and [source catalog](../../catalog/event-systems/README.md).

Use `MPE-PRD-*` only for these proposed extensions. Existing `MPE-*` obligations remain in [Appendix A](../design-document/build/appendix-a.md) and [ears-consolidated.json](../design-document/build/ears-consolidated.json). Referenced obligations are not evidence of implemented behavior. Candidate status is explicit in the JSON records; EARS “shall” describes a proposed obligation if adopted.

Before adoption, record an owner, customer evidence, leakage profile, engineering estimate, dependencies and disposition. Numbers in source systems are not inherited service targets. The first suggested pilot is institutional RFQ coordination on backend/desktop, with settlement gated on completed authority, replay and anchored-message-binding verification.
