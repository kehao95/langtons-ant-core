# Claim ledger

| Item | Status | Evidence boundary |
| --- | --- | --- |
| One classical update | implemented and tested | `engine/langtons_ant/`, `tests/test_model.py` |
| One-step convention in Lean | formalized | `formal/LangtonsAntHC/Dynamics.lean` |
| Blank oriented P104 boundary | finite witness plus analytic recurrence | `theory/blank-highway.md`, `tests/test_highway.py` |
| One black, ant initially on it | finite prefix plus symmetry transport | `theory/one-black-under-ant.md`, `tests/test_one_black.py` |
| Arbitrary-offset one-black reduction | finite-prefix split | `theory/one-black-reduction.md`, `tests/test_coupling.py` |
| P104 entry plus one off-ray obstacle | finite footprint-ray theorem | `theory/entry-obstacle.md`, `tests/test_obstacles.py` |
| Highway Conjecture | open | `theory/global-conjecture.md` |
| Research-layer dependency map | stated | `theory/architecture.md` |
| One-black initial family at arbitrary offset | open | `theory/restricted-families.md` |
| Highway terminal predicate | open | no datum or checker admitted |
| Soundness of terminal recognition | open | depends on a predicate |
| Finite-support global highway claim | open | depends on recognition and a complete bridge |

This ledger is deliberately conservative. A row changes only with the
corresponding statement, artefact, and narrowly scoped verification path.
