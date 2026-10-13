# Repository method

This repository develops exact Langton-ant proofs from literal finite-state
replay and explicit mathematical induction.

- `one_black/` owns the universal one-black theorem, its dynamics, verifier,
  and proof narrative.
- `clock_escape/` owns the independent rational-clock and exponential square-escape
  preprint, analytic proof, local Lean lemmas and self-contained verification.
- `preprint/` owns the one-black manuscript and its publication evidence.
- Root `PROOF.md` owns deductions built from the theorem kernels.
- `RESEARCH.md` owns the current research graph and the next theorem targets.
- Every executable check names the proof step it witnesses.
- A changed theorem lands with its proof narrative and finite verifier in one
  commit.
- Imported mathematical evidence carries a precise source; locally promoted
  results carry a reconstructed proof object.
- `python3 one_black/check.py` builds the closed Lean universal theorem.
- `python3 research/check.py` replays the executable general consequences.
- `python3 clock_escape/reproduce.py` replays the clock paper evidence.
- Dependencies flow from `one_black/` into `research/`; `clock_escape/` is
  self-contained and does not depend on the one-black theorem.
