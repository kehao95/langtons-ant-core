# Twenty-cell one-shot feedback circuit

A complete twenty-black initial state, parameterized by even n>=20, creates a
black cell at time 60 and reads it back at time 624n-1516 with exactly 31 S_128
reads strictly between. Its exact FIRST standard-P104 time is 624n-742.
It is a family of positive finite inputs, not an infinite renewable controller.

`circuit.py` constructs the literal seed, the five reference stages, complete
XOR endpoint, affine all-parameter separation checks, protected recovery field
and an infinite-period verifier. `check.py` adds independent finite dynamics
and a second infinite-period criterion. `report.json` is deterministic and
hashes both source files. No third-party libraries, solver or network is used.

Run `python scripts/check_scalable_feedback_circuit.py` from the repository root.
The runner checks this package in a temporary copy and compares JSON bytes.
The universal proof and precise failed closure are in
`proof/results/scalable-feedback-circuit.md`.

All input cells are specified at time zero and every other cell is white.
The parameter is in the input coordinates. No external intervention or deletion
of the true historical field is permitted or used.
