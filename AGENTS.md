# Repository method

This repository develops exact Langton-ant proofs from literal finite-state
replay and explicit mathematical induction.

- `one_black/` owns the universal one-black theorem, its dynamics, verifier,
  and proof narrative.
- Root `PROOF.md` owns deductions built from that theorem kernel.
- `RESEARCH.md` owns the current research graph and the next theorem targets.
- Every executable check names the proof step it witnesses.
- A changed theorem lands with its proof narrative and finite verifier in one
  commit.
- Imported mathematical evidence carries a precise source; locally promoted
  results carry a reconstructed proof object.
- `python3 one_black/check.py` builds the closed Lean universal theorem.
- `python3 research/check.py` replays the executable general consequences.
- Dependencies flow from `one_black/` into `research/`.
