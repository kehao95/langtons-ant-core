# Six-cell feedback certificates

The complete initial black set is
`{(-87,-55),(-87,-52),(-84,-55),(-82,-61),(-81,-55),(-80,-60)} + k*(-2,-2)`
for integer k>=0, with head at the origin facing north and a white exterior.
It produces exactly 6702+47k contained ten-factor defects and 6706+47k intrinsic
J10 events, with first permanent P104 entrance at 18743+220k.

Run `python3 defect_synthesis/reproduce.py --six-cell-only` from the repository
root. Python 3.10+ and a C++17 compiler are required. The entrypoint runs a
disposable copy and compares the deterministic report without modifying evidence.
`witness.json` supplies finite words and coordinate data; `verify.py` checks the
all-parameter full-field XOR recurrence and integer half-ray guards.
`independent.cpp` reconstructs literal trajectories and verifies complete tails.
`query.py K --include-field` emits the terminal field as finite XOR segments.

The analytic coverage argument, exact arithmetic, language runtimes and compiler
form the trust boundary. Finite controls support the implementation; the recurrence
and ray guards carry the universal parameter claim. See the article for the proof.
