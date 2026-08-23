# Langton's Ant: Highway Conjecture

This is a clean-room research repository for the classical finite-support
Langton's Ant highway conjecture.

The question is simple to state: does every finite initial black set eventually
join the standard translating period-104 highway?  The answer is not asserted
here.  This repository will record only claims whose assumptions, proof object,
and verification boundary are explicit.

## Start here

- [`RESEARCH_CHARTER.md`](./RESEARCH_CHARTER.md) defines the research program.
- [`theory/`](./theory/) will hold the canonical theorem graph and open lemmas.
- [`engine/`](./engine/) will hold a small exact implementation of the classical
  rule.
- [`evidence/`](./evidence/) will hold immutable certificates and narrow
  checkers.
- [`research/`](./research/) will hold exploratory work that has not become a
  theorem.
- [`history/`](./history/) will hold only material intentionally retained for
  provenance.

No result from a predecessor repository has been imported into this repository
yet.  Each retained result will be reconstructed here from its statement,
minimal dependencies, and independent evidence.
