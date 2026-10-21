# Initial-contour exit: exact ordered contacts, not permanent spatial escape

Run `python scripts/check_contour_exit.py` at repository root. Python 3.10+,
C++17 (`g++`) and Boost multiprecision headers are required. No ISL, SMT solver,
old large graph reconstruction or other historical test suite is used.

`kernel.py` freezes the source contour once and computes the first actual incoming
state outside that fixed dart set. Internally paired ports exchange successors;
an exposed port leads outside on its second read. The complete original field is
updated by the actual read-site parity, never replaced by a cleared core.

For noninterlaced contacts there is an exact formula and the sharp T<=L+1 bound;
`sharp_seed(n)` provides genuine finite inputs attaining equality at all n>=0.
The all-parameter proof is in `proof/results/noninterlaced-contour-exit.md`.
The 24-black, L=100, T=220 witness shows that even T<=2L fails without the
hypothesis. It is a finite transfer, not an HC counterexample.

`check.py` compares exact complete fields and itineraries to a separate literal
simulator. The independent native simulator uses vector rotations and original
black sets, not the matching kernel. `report.json` freezes deterministic fields
and source hashes; default replay does not repair it. `--generate` is the explicit
report-creation mode only. Caps are INCONCLUSIVE. Abstract cyclic switches are not
necessarily square-lattice-realizable; a supplied nonphysical trap is a scope check.

The baseline contour representation and classical no-bounded-orbit theorem are
credited upstream. Local exit is not transience, infinite-contour-chain termination,
P104 attraction or a declared stand-alone publication. The global HC frontier is
not promoted by this module.
