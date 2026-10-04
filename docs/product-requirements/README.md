# Product requirements and implementation choices

These documents propose workflows, technology choices and acceptance gates for Midnight Express. Start with the stack recommendation to understand the intended product, then use the requirement and component studies to assess a pilot. The portfolio is still a set of candidates; adoption requires a decision against the existing protocol obligations.

- [Recommended stack and ranked use cases](recommended-stack-and-use-cases.md): consolidated technology choices, business fit and delivery gates.
- [Business use cases](top-ten-use-cases.md): ranked business scenarios, actors, triggers, value hypotheses, acceptance scenarios and dependencies.
- [Machine-readable use-case register](use-cases.json): ten candidate records linked to existing and proposed requirements.
- [Candidate EARS extensions](candidate-ears.md): sixteen product/API obligations with acceptance checks and an open product decision.
- [Machine-readable candidate requirement register](candidate-requirements.json).
- [UmbraDB recovery and future release](umbradb-recovery.md): source/API checks, backend integration boundary and acceptance requirements.
- [Working stack and Semaphore extraction](proposed-stack.md): adopted membership lifecycle, admission boundaries and module interfaces.
- [Semaphore membership option](semaphore-membership-option.md): scoped nullifiers, quota gaps and compatibility conditions.
- [Original requirement fit and open-source stack](requirements-fit-and-open-source.md): all twelve areas, remaining components and build sequence.
- [GossipSub + Signal composition option](gossipsub-signal-option.md): pairwise session design and experimental gates.
- [Top ten feature considerations](feature-considerations.md): enabling capabilities kept separate from use cases.
- [Source-study findings](../../reviews/competitive-event-systems/extraction.md) and [source catalog](../../catalog/event-systems/README.md).

Use `MPE-PRD-*` only for these proposed extensions. Existing `MPE-*` obligations remain in [Appendix A](../design-document/build/appendix-a.md) and [ears-consolidated.json](../design-document/build/ears-consolidated.json). Referenced obligations are not evidence of implemented behavior. Candidate status is explicit in the JSON records; EARS “shall” describes a proposed obligation if adopted.

The first suggested pilot is institutional RFQ coordination on backend/desktop. Before adopting it or another candidate, record an owner, customer evidence, leakage profile, engineering estimate, dependencies and disposition. Source-system performance numbers do not become Midnight Express service targets. Settlement must wait for completed authority, replay and anchored-message-binding verification.
