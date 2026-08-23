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
- [`theory/trust-boundary.md`](./theory/trust-boundary.md) distinguishes the
  finite checker, formal Lean core, and still-unformalized arguments.
- [`evidence/`](./evidence/) defines the boundary for immutable data when a
  result needs data beyond a derivable finite witness.
- [`research/`](./research/) will hold exploratory work that has not become a
  theorem.
- [`history/`](./history/) will hold only material intentionally retained for
  provenance.

The reconstructed claims are listed in the [claim ledger](./theory/ledger.md):
the exact dynamics, a four-orientation P104 terminal condition, the one-black
family with the ant initially on its black square, and off-ray entry obstacles.
The arbitrary-offset one-black theorem and the global Highway Conjecture remain
open. No predecessor code, certificate, or proof text has been imported.
