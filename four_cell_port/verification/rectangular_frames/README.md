# Rectangular frames and exact highway entrance

The classical white-right/black-left ant starts at the southwest corner facing
north, with a white exterior. For n,m>=10 a four-layer black frame shields any
interior pattern, giving the same trace and the stated exact P104 entrance times.
All solid rectangles at that pose have the sharp bound 242(n+m)+29325.
The centered odd-square family has a separate complete classification.

Run `python3 four_cell_port/reproduce.py --frames-only --jobs 3` from the repository
root. This executes the full module: 42 all-parameter certificates, 71484 read
obligations, 2838 interior-avoidance obligations, 3501 finite rectangles and 37
centered squares. Each finite implementation performs 32681376 updates.
The module's `check.py --quick` checks only four frame certificates and scope
controls; it is not the full proof replay.

Requirements: Python 3.10+ without -O, ISL/GMP (retained reports use 0.27-GMP),
and a C++17 compiler. `verify.py` and `exact_sets.py` check exact bad-read-set
emptiness. `coverage.py` checks parameter cover and sharpness identities.
`finite_check.py` compares Python/C++ complete trajectories and infinite tails.
`controls.py` checks arbitrary interiors, remote cells and corruptions.
The analytic coverage reduction and exact-arithmetic toolchain are the trust
boundary. `sources.json` binds all inputs; evidence is never silently regenerated.
