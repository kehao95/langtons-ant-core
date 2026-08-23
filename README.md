# Langton's Ant: Highway Conjecture

This is a clean-room research repository for the classical finite-support
Langton's Ant highway conjecture.

The question is simple to state: does every finite initial black set eventually
join the standard translating period-104 highway?  The answer is not asserted
here.  This repository will record only claims whose assumptions, proof object,
and verification boundary are explicit.

## Start here

- [`RESEARCH_CHARTER.md`](./RESEARCH_CHARTER.md) defines the research program.
- [`theory/`](./theory/) contains the problem statement, the terminal-predicate
  contract, the dependency architecture, and the open global bridge.
- [`engine/langtons_ant/`](./engine/langtons_ant/) is the exact reference model
  for one classical update.
- [`tests/`](./tests/) checks the convention at the smallest useful boundary.
- [`scripts/check.py`](./scripts/check.py) runs only those focused checks.
- [`formal/`](./formal/) holds a separately checked Lean core for the state
  convention; its scope is intentionally listed in its own README.
- [`evidence/`](./evidence/) will hold immutable certificates and narrow
  checkers when a result is promoted.
- [`research/`](./research/) will hold exploratory work that has not become a
  theorem.
- [`history/`](./history/) will hold only material intentionally retained for
  provenance.

The classical state-transition kernel and a checked blank-orbit P104 recurrence
are reconstructed components. No one-black certificate or global theorem has
been imported or asserted. Each later result must be rebuilt from its statement,
minimal dependencies, and independent evidence.
