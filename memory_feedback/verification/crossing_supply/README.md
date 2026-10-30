# Incoming requests and crossing capacity

For an initially white half-plane, incoming heights determine every completed
reply and the complete retained inside field. The article proves request
injectivity, the capacity `q^(j+1)-(q-1)^(j+1)` with `q=floor(H/2)+1`,
the exact finite-prefix packing bound and the speed/spread exponent
`4v/(1-2v)`. The oblique-width leading coefficient remains `1/log(2)`.

Run `python3 memory_feedback/reproduce.py --crossing-only` from the repository
or source-package root. This copies both crossing modules into a disposable
workspace. `check.py` checks the frozen report without changing it and pins
its sibling `crossing_gap/core.py` and `oracle.cpp`. Python 3.10+ and C++17
are required; keep assertions enabled.

The report includes 78 complete physical inputs, 86,647 updates per literal
implementation, 186 complete residual-half-plane comparisons, exact capacity
and packing identities, and malformed-history controls. The analytic proof
covers all actual finite histories. Codes are counted as an upper capacity;
realizability and arbitrary half-plane return are separate questions. A capped
simulation returns UNKNOWN. The retained report binds the checker bytes.
